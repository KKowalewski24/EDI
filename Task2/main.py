import os
import subprocess
import sys
from argparse import ArgumentParser, Namespace
from datetime import datetime

import arff
import html2text
import pandas as pd

"""
    How to run:
        python main.py --plain -f data/abc.html
        python main.py --arff -f data/abc.txt -p "Page "
"""

# VAR ------------------------------------------------------------------------ #
UTF_8 = "utf-8"
OUTPUT_DIR = "output/"
CSV = ".csv"
ARFF = ".arff"


# MAIN ----------------------------------------------------------------------- #
def main() -> None:
    args = prepare_args()
    to_plain = args.plain
    to_arff = args.arff
    filename = args.filename
    phrase = args.phrase

    if to_plain:
        convert_html_to_plain(filename)

    if to_arff:
        convert_plain_text_to_arff(filename, phrase)

    display_finish()


# DEF ------------------------------------------------------------------------ #
def convert_html_to_plain(filename: str) -> None:
    with open(filename) as file:
        plain_text = html2text.html2text(file.read())

    with open(get_filename_from_path(filename), "w", encoding=UTF_8) as file:
        file.write(plain_text)


def convert_plain_text_to_arff(filename: str, phrase: str) -> None:
    df = pd.DataFrame(columns=['title', 'data'])

    with open(filename, encoding=UTF_8) as file:
        # TODO FINISH CONVERTER
        pass

    save_df_to_csv_and_arff(df, get_filename_from_path(filename), False)


def save_df_to_csv_and_arff(df: pd.DataFrame, collection_name: str, add_date: bool = True) -> None:
    df.to_csv(OUTPUT_DIR + prepare_filename(collection_name, CSV, add_date), index=False)
    arff.dump(
        OUTPUT_DIR + prepare_filename(collection_name, ARFF, add_date), df.values,
        relation=collection_name, names=df.columns
    )


def get_filename_from_path(filename: str) -> str:
    return os.path.splitext(os.path.basename(filename))[0]


def prepare_filename(name: str, extension: str, add_date: bool = True) -> str:
    return (name + "-" + (datetime.now().strftime("%H%M%S") if add_date else "")
            + extension).replace(" ", "")


def prepare_args() -> Namespace:
    arg_parser = ArgumentParser()

    arg_parser.add_argument(
        "--plain", default=False, action="store_true", help="Convert HTML to plain text"
    )
    arg_parser.add_argument(
        "--arff", default=False, action="store_true", help="Convert plain text to arff"
    )
    arg_parser.add_argument(
        "-f", "--filename", required=True, type=str, help="HTML or plain text filename"
    )
    arg_parser.add_argument(
        "-p", "--phrase", type=str, help="Phrase to find page"
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
