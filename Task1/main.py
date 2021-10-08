import subprocess
import sys
import arff
import pandas as pd

"""
"""

# VAR ------------------------------------------------------------------------ #
LOGS_PATH = "data/logs.csv"


# MAIN ----------------------------------------------------------------------- #
def main() -> None:
    df = pd.read_csv(LOGS_PATH)
    df = filter_logs(df)
    print(len(df))
    display_finish()


# DEF ------------------------------------------------------------------------ #
def filter_logs(df: pd.DataFrame) -> pd.DataFrame:
    return df.loc[
        (df["method"] == "GET")
        & (df["response"] == 200)
        & (~df['url'].str.contains('.jpg|.gif|.bmp|.xbm|.png|.jpeg'))
        ]


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
