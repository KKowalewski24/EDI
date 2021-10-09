import os
import subprocess
import sys
from datetime import datetime, timedelta
from typing import Dict, Tuple

import arff
import pandas as pd
from nameof import nameof
from tqdm import tqdm

"""
"""

# VAR ------------------------------------------------------------------------ #
LOGS_PATH = "data/logs.csv"
OUTPUT_DIR = "output/"
CSV = "csv"
ARFF = "arff"
SECONDS_IN_MINUTE = 60
FIXED_SESSION_DURATION = 10 * SECONDS_IN_MINUTE
POPULAR_SITE_FRACTION = 0.5
ROWS_NUMBER_TO_READ = 50000


# MAIN ----------------------------------------------------------------------- #
def main() -> None:
    create_directory(OUTPUT_DIR)
    print("Preparing logs ...")
    df: pd.DataFrame = prepare_logs(filter_logs(pd.read_csv(LOGS_PATH, nrows=ROWS_NUMBER_TO_READ)))
    print("Preparing sessions and users ...")
    sessions, users = prepare_sessions_and_users(df)
    # print(sessions)
    # print(users)
    # sessions_pages = sessions.drop(columns=['duration', 'requests_count', 'avg_request_duration'])
    # sessions_numeric = sessions[['duration', 'requests_count', 'avg_request_duration']]
    # users_pages = users.drop(columns=['requests_count'])

    print("Saving processed data to files ...")
    for data_frame, label in zip([sessions, users], [nameof(sessions), nameof(users)]):
        save_df_to_csv_and_arff(data_frame, label)

    display_finish()


# DEF ------------------------------------------------------------------------ #
def filter_logs(df: pd.DataFrame) -> pd.DataFrame:
    return df.loc[
        (df["method"] == "GET")
        & (df["response"] == 200)
        & (~df["url"].str.contains(".jpg|.gif|.bmp|.xbm|.png|.jpeg"))
        ]


def prepare_logs(df: pd.DataFrame) -> pd.DataFrame:
    df['time'] = pd.to_datetime(df['time'])
    return df


def get_popular_sites(df: pd.DataFrame) -> pd.DataFrame:
    sites_counts = df["url"].value_counts().rename("count")
    sites_percents = (df['url'].value_counts(normalize=True) * 100).rename("percent")

    sites = pd.concat([sites_counts, sites_percents], axis=1)
    sites = sites.reset_index().rename({"index": "url"}, axis=1)

    return sites[sites["percent"] > POPULAR_SITE_FRACTION]


def get_empty_popular_sites_dictionary(popular_sites: pd.DataFrame) -> Dict[str, bool]:
    return {b: False for b in popular_sites['url']}


def prepare_sessions_and_users(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    unique_users: pd.DataFrame = df["host"].unique()
    popular_sites: pd.DataFrame = get_popular_sites(df)

    sessions = []
    users = []

    for i in tqdm(range(len(unique_users))):
        requests = pd.DataFrame(df[df["host"] == unique_users[i]])

        session_start = requests.iloc[0]["time"]
        session_end = session_start
        session_visited_sites = get_empty_popular_sites_dictionary(popular_sites)
        user_visited_sites = get_empty_popular_sites_dictionary(popular_sites)
        session_requests_count = 0
        user_requests_count = 0

        for index, request in requests.iterrows():
            if request["time"] - session_end > timedelta(seconds=FIXED_SESSION_DURATION):
                if session_requests_count > 1:
                    session_duration = (session_end - session_start).total_seconds()
                    avg_request_duration = session_duration / (session_requests_count - 1)
                    sessions.append(
                        {
                            **{
                                "duration": session_duration,
                                "requests_count": session_requests_count,
                                "avg_request_duration": avg_request_duration
                            },
                            **session_visited_sites
                        }
                    )

                session_start = request["time"]
                session_visited_sites = get_empty_popular_sites_dictionary(popular_sites)
                session_requests_count = 0

            if request["url"] in session_visited_sites:
                session_visited_sites[request["url"]] = True
                user_visited_sites[request["url"]] = True

            session_requests_count += 1
            user_requests_count += 1
            session_end = request["time"]

        users.append(
            {**{'requests_count': user_requests_count}, **session_visited_sites}
        )

    return pd.DataFrame(sessions), pd.DataFrame(users)


def save_df_to_csv_and_arff(df: pd.DataFrame, collection_name: str) -> None:
    df.to_csv(OUTPUT_DIR + get_filename(collection_name, CSV), index=False)
    arff.dump(
        OUTPUT_DIR + get_filename(collection_name, ARFF), df.values,
        relation=collection_name, names=df.columns
    )


def create_directory(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)


def get_filename(name: str, extension: str) -> str:
    return (name + "-" + datetime.now().strftime("%H%M%S") + extension).replace(" ", "")


# UTIL ----------------------------------------------------------------------- #
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
