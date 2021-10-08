import os
import subprocess
import sys
from datetime import datetime

import arff
import pandas as pd
from nameof import nameof

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


# MAIN ----------------------------------------------------------------------- #
def main() -> None:
    create_directory(OUTPUT_DIR)
    df: pd.DataFrame = filter_logs(pd.read_csv(LOGS_PATH))
    # df.to_csv(OUTPUT_DIR + "out.csv")
    # print(len(df))
    # print(df.head())

    display_finish()


# DEF ------------------------------------------------------------------------ #
def filter_logs(df: pd.DataFrame) -> pd.DataFrame:
    return df.loc[
        (df["method"] == "GET")
        & (df["response"] == 200)
        & (df['url'].str.contains('.jpg|.gif|.bmp|.xbm|.png|.jpeg') == False)
        ]


def save_df_to_csv_and_arff(df: pd.DataFrame) -> None:
    collection_name = nameof(df)
    df.to_csv(get_filename(collection_name, CSV), index=False)
    arff.dump(
        get_filename(collection_name, ARFF), df.values,
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
