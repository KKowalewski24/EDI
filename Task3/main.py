import os
import subprocess
import sys
from argparse import ArgumentParser, Namespace
from datetime import datetime

"""
    How to run:
    
"""

# VAR ------------------------------------------------------------------------ #
OUTPUT_DIR: str = "output/"


# MAIN ----------------------------------------------------------------------- #
def main() -> None:
    args = prepare_args()
    filepath = args.filepath

    display_finish()


# DEF ------------------------------------------------------------------------ #
def get_filename_from_path(filepath: str) -> str:
    return os.path.splitext(os.path.basename(filepath))[0]


def prepare_filename(name: str, extension: str, add_date: bool = True) -> str:
    return (name + ("-" + datetime.now().strftime("%H%M%S") if add_date else "")
            + extension).replace(" ", "")


def prepare_args() -> Namespace:
    arg_parser = ArgumentParser()

    arg_parser.add_argument(
        "-f", "--filepath", required=True, type=str, help="Clusters filepath"
    )

    return arg_parser.parse_args()


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
