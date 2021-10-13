import os
import subprocess
import sys
from argparse import ArgumentParser, Namespace
from datetime import datetime
from typing import Any, Dict, List, Tuple

import arff
import pandas as pd
from nameof import nameof
from tqdm import tqdm

"""
    How to run:
        Filter data:    python main.py -f
        Group data:     python main.py -g
"""

# VAR ------------------------------------------------------------------------ #
LOGS_PATH: str = "data/logs.csv"
OUTPUT_DIR: str = "output/"
FILTERED_LOGS: str = "filtered_logs"
CSV: str = ".csv"
ARFF: str = ".arff"
SECONDS_IN_MINUTE: int = 60
FIXED_SESSION_DURATION: int = 10 * SECONDS_IN_MINUTE
POPULAR_SITE_PERCENT: float = 0.5
ROWS_NUMBER_TO_READ: int = 50000


# MAIN ----------------------------------------------------------------------- #
def main() -> None:
    args = prepare_args()
    create_directory(OUTPUT_DIR)
    is_filtering_active = args.filter
    is_grouping_active = args.group

    if is_filtering_active:
        print("Preparing logs ...")
        df: pd.DataFrame = filter_logs(pd.read_csv(LOGS_PATH, nrows=ROWS_NUMBER_TO_READ))

        print("Saving processed data to files, number of records" + str(len(df.index)) + " ...")
        save_df_to_csv_and_arff(df, FILTERED_LOGS, add_date=False)

    if is_grouping_active:
        print("Preparing sessions and users ...")
        df: pd.DataFrame = pd.read_csv(OUTPUT_DIR + FILTERED_LOGS + CSV)
        (
            extracted_users, extracted_sessions, user_pages,
            sessions_pages, sessions_numeric
        ) = extract_data(df)

        print("Saving processed data to files ...")
        zipped_data = zip(
            [
                extracted_users, extracted_sessions, user_pages,
                sessions_pages, sessions_numeric
            ],
            [
                nameof(extracted_users), nameof(extracted_sessions), nameof(user_pages),
                nameof(sessions_pages), nameof(sessions_numeric)
            ]
        )
        for data_frame, label in zipped_data:
            save_df_to_csv_and_arff(data_frame, label)

    display_finish()


# DEF ------------------------------------------------------------------------ #
def filter_logs(df: pd.DataFrame) -> pd.DataFrame:
    return df.loc[
        (df["method"] == "GET")
        & (df["response"] == 200)
        & (~df["url"].str.contains(".jpg|.gif|.bmp|.xbm|.png|.jpeg"))
        ]


def extract_data(df: pd.DataFrame) -> \
        Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    extracted_sessions: List[Dict[str, Any]] = []
    extracted_users: List[Dict[str, Any]] = []

    unique_users: pd.Series = df["host"].unique()
    popular_sites: pd.DataFrame = get_popular_sites(df)

    for user in tqdm(unique_users):
        requests: pd.DataFrame = df[df["host"] == user]

        session_start = int(requests.iloc[0]["time"])
        session_end = session_start
        session_visited_sites: Dict[str, bool] = prepare_popular_sites_with_flag(popular_sites)
        user_visited_sites: Dict[str, bool] = prepare_popular_sites_with_flag(popular_sites)
        session_requests_count: int = 0
        user_requests_count: int = 0

        for index, request in requests.iterrows():
            if request["time"] - session_end > FIXED_SESSION_DURATION:
                if session_requests_count > 1:
                    session_duration = (session_end - session_start)
                    average_request_duration = session_duration / (session_requests_count - 1)
                    extracted_sessions.append(
                        {**{
                            "duration": session_duration,
                            "requests_count": session_requests_count,
                            "average_request_duration": average_request_duration
                        },
                         **session_visited_sites}
                    )

                session_start = request["time"]
                session_visited_sites = prepare_popular_sites_with_flag(popular_sites)
                session_requests_count = 0

            if request["url"] in session_visited_sites:
                session_visited_sites[request["url"]] = True
                user_visited_sites[request["url"]] = True

            session_requests_count += 1
            user_requests_count += 1
            session_end = request["time"]

        extracted_users.append(
            {**{
                "requests_count": user_requests_count
            },
             **session_visited_sites}
        )

    return modify_extracted_data(pd.DataFrame(extracted_users), pd.DataFrame(extracted_sessions))


def modify_extracted_data(extracted_users: pd.DataFrame, extracted_sessions: pd.DataFrame) -> \
        Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    session_additional_cols: List[str] = ["duration", "requests_count", "average_request_duration"]

    user_pages: pd.DataFrame = extracted_users.drop(columns=["requests_count"])
    sessions_pages: pd.DataFrame = extracted_sessions.drop(columns=session_additional_cols)
    sessions_numeric: pd.DataFrame = extracted_sessions[session_additional_cols]

    return extracted_users, extracted_sessions, user_pages, sessions_pages, sessions_numeric


def get_popular_sites(df: pd.DataFrame) -> pd.DataFrame:
    sites_percents: pd.DataFrame = (
        (df["url"].value_counts(normalize=True) * 100)
            .rename("percent")
            .reset_index()
            .rename({"index": "url"}, axis=1)
    )
    return sites_percents[sites_percents["percent"] > POPULAR_SITE_PERCENT]


def prepare_popular_sites_with_flag(popular_sites: pd.DataFrame) -> Dict[str, bool]:
    return {site: False for site in popular_sites["url"]}


def save_df_to_csv_and_arff(df: pd.DataFrame, collection_name: str, add_date: bool = True) -> None:
    df.to_csv(OUTPUT_DIR + get_filename(collection_name, CSV, add_date), index=False)
    arff.dump(
        OUTPUT_DIR + get_filename(collection_name, ARFF, add_date), df.values,
        relation=collection_name, names=df.columns
    )


def prepare_args() -> Namespace:
    arg_parser = ArgumentParser()

    arg_parser.add_argument(
        "-f", "--filter", default=False, action="store_true", help="Filter logs"
    )
    arg_parser.add_argument(
        "-g", "--group", default=False, action="store_true", help="Group logs"
    )

    return arg_parser.parse_args()


# UTIL ----------------------------------------------------------------------- #
def create_directory(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)


def get_filename(name: str, extension: str, add_date: bool = True) -> str:
    return (name + ("-" + datetime.now().strftime("%H%M%S") if add_date else "")
            + extension).replace(" ", "")


def check_types_check_style() -> None:
    subprocess.call(["mypy", "."])
    subprocess.call(["flake8", "."])


def compile_to_pyc() -> None:
    subprocess.call(["python", "-m", "compileall", "."])


def check_if_exists_in_args(arg: str) -> bool:
    return arg in sys.argv


def display_finish() -> None:
    print("------------------------------------------------------------------------")
    print("FINISHED")
    print("------------------------------------------------------------------------")


# __MAIN__ ------------------------------------------------------------------- #
if __name__ == "__main__":
    if check_if_exists_in_args("-t"):
        check_types_check_style()
    elif check_if_exists_in_args("-b"):
        compile_to_pyc()
    else:
        main()
