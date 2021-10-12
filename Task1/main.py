import os
import subprocess
import sys
from argparse import ArgumentParser, Namespace
from datetime import datetime
from typing import List, Tuple

import arff
import pandas as pd
from tqdm import tqdm

"""
    How to run:
        Filter data:    python main.py -f
        Group data:     python main.py -g
"""

# VAR ------------------------------------------------------------------------ #
LOGS_PATH = "data/logs.csv"
OUTPUT_DIR = "output/"
FILTERED_LOGS = "filtered_logs"
CSV = ".csv"
ARFF = ".arff"
SECONDS_IN_MINUTE = 60
FIXED_SESSION_DURATION = 10 * SECONDS_IN_MINUTE
POPULAR_SITE_FRACTION = 0.5
ROWS_NUMBER_TO_READ = 50000


# MAIN ----------------------------------------------------------------------- #
def main() -> None:
    args = prepare_args()
    create_directory(OUTPUT_DIR)
    is_filtering_active = args.filter
    is_grouping_active = args.group

    if is_filtering_active:
        print("Preparing logs ...")
        df: pd.DataFrame = prepare_logs(
            filter_logs(pd.read_csv(LOGS_PATH, nrows=ROWS_NUMBER_TO_READ))
        )
        print("Saving processed data to files, number of records" + str(len(df.index)) + " ...")
        save_df_to_csv_and_arff(df, FILTERED_LOGS, add_date=False)

    if is_grouping_active:
        print("Preparing sessions and users ...")
        df: pd.DataFrame = pd.read_csv(OUTPUT_DIR + FILTERED_LOGS + CSV)
        extract_data(df)
        print("Saving processed data to files ...")
        for data_frame, label in zip([], []):
            save_df_to_csv_and_arff(data_frame, label)

    display_finish()


# DEF ------------------------------------------------------------------------ #
def prepare_args() -> Namespace:
    arg_parser = ArgumentParser()

    arg_parser.add_argument(
        "-f", "--filter", default=False, action="store_true", help="Filter logs"
    )
    arg_parser.add_argument(
        "-g", "--group", default=False, action="store_true", help="Group logs"
    )

    return arg_parser.parse_args()


def filter_logs(df: pd.DataFrame) -> pd.DataFrame:
    return df.loc[
        (df["method"] == "GET")
        & (df["response"] == 200)
        & (~df["url"].str.contains(".jpg|.gif|.bmp|.xbm|.png|.jpeg"))
        ]


def prepare_logs(df: pd.DataFrame) -> pd.DataFrame:
    df["time"] = pd.to_datetime(df["time"]).astype("str")
    return df


def extract_data(df: pd.DataFrame) -> Tuple[List, List]:
    unique_users = df["host"].unique()
    extracted_sessions: List = []
    extracted_users: List = []

    for user in tqdm(unique_users):
        requests: pd.DataFrame = df[df["host"] == user]
        for request in requests:
            pass

    return extracted_users, extracted_sessions


def save_df_to_csv_and_arff(df: pd.DataFrame, collection_name: str, add_date: bool = True) -> None:
    df.to_csv(OUTPUT_DIR + get_filename(collection_name, CSV, add_date), index=False)
    arff.dump(
        OUTPUT_DIR + get_filename(collection_name, ARFF, add_date), df.values,
        relation=collection_name, names=df.columns
    )


def create_directory(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)


def get_filename(name: str, extension: str, add_date: bool = True) -> str:
    return (name + ("-" + datetime.now().strftime("%H%M%S") if add_date else "")
            + extension).replace(" ", "")


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
