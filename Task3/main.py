import os
import random
import subprocess
import sys
from argparse import ArgumentParser, Namespace
from datetime import datetime
from typing import List

from sklearn.metrics import jaccard_score

"""
    How to run:
    
"""

# VAR ------------------------------------------------------------------------ #
OUTPUT_DIR: str = "output/"
# TODO TEST AND MAYBE CHANGE
CONSTANT_USER: List[bool] = [
    True, False, False, False, False, True, False, True, True, True, False, False, False,
    False, True, True, False, False, True, False, False, True, True, False, False, False,
    False, True, False, True
]


# MAIN ----------------------------------------------------------------------- #
def main() -> None:
    args = prepare_args()
    filepath = args.filepath
    is_random_user = args.random_user
    random_user_pages_number = args.random_user_pages_number

    print("Preparing user ...")
    user: List[bool] = get_user(is_random_user, random_user_pages_number)

    display_finish()


# DEF ------------------------------------------------------------------------ #
def get_user(is_random_user: bool, random_user_pages_number: int) -> List[bool]:
    if is_random_user:
        return [random.choice([True, False]) for _ in range(random_user_pages_number)]

    return CONSTANT_USER


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
    arg_parser.add_argument(
        "-ru", "--random_user", default=False, action="store_true", help="Generate random user"
    )
    arg_parser.add_argument(
        "-pn", "--random_user_pages_number", type=int,
        help="Number of pages for randomly generated user"
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
