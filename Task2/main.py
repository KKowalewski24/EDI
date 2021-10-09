import os
import subprocess
import sys
from argparse import ArgumentParser, Namespace

import html2text

"""
    How to run:
        python main.py --plain -f data/abc.html
        python main.py --arff -f data/abc.txt
"""


# VAR ------------------------------------------------------------------------ #

# MAIN ----------------------------------------------------------------------- #
def main() -> None:
    args = prepare_args()
    plain = args.plain
    arff = args.arff
    filename = args.filename

    if plain:
        convert_html_to_plain(filename)

    if arff:
        convert_plain_text_to_arff(filename)

    display_finish()


# DEF ------------------------------------------------------------------------ #
def convert_html_to_plain(filename: str) -> None:
    with open(filename) as file:
        plain_text = html2text.html2text(file.read())

    trimmed_filename = os.path.splitext(os.path.basename(filename))[0]
    with open(trimmed_filename, "w", encoding="utf-8") as file:
        file.write(plain_text)


def convert_plain_text_to_arff(filename: str) -> None:
    pass


def prepare_args() -> Namespace:
    arg_parser = ArgumentParser()

    arg_parser.add_argument(
        "--plain", default=False, action="store_true", help="Convert HTML to plain text"
    )
    arg_parser.add_argument(
        "--arff", default=False, action="store_true", help="Convert plain text to arff"
    )
    arg_parser.add_argument(
        "-f", "--filename", type=str, help="HTML or plain text filename"
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
