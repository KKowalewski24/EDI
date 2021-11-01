import os
import re
import string
import subprocess
import sys
from argparse import ArgumentParser, Namespace
from datetime import datetime
from typing import List, Tuple

import arff
import html2text
import pandas as pd

"""
    How to run:
        python main.py -f data/abc.html --plain
        python main.py -f data/abc.txt --arff
"""

# VAR ------------------------------------------------------------------------ #
UTF_8: str = "utf-8"
OUTPUT_DIR: str = "output/"
CSV: str = ".csv"
ARFF: str = ".arff"
TXT: str = ".txt"
PATTERN: str = "(.*)\s(Page \d+\n)"
PUNCTUATION_CHARACTERS: str = string.punctuation + "\n" + "â€˘" + "Â»"


# MAIN ----------------------------------------------------------------------- #
def main() -> None:
    args = prepare_args()
    filepath = args.filepath
    to_plain = args.plain
    to_arff = args.arff

    if to_plain:
        convert_html_to_plain(filepath)
    elif to_arff:
        convert_plain_text_to_arff(filepath)

    display_finish()


# DEF ------------------------------------------------------------------------ #
def convert_html_to_plain(filename: str) -> None:
    with open(filename) as file:
        plain_text = html2text.html2text(file.read())

    with open(get_filename_from_path(filename) + TXT, "w", encoding=UTF_8) as file:
        file.write(plain_text)


def convert_plain_text_to_arff(filename: str) -> None:
    data: List[Tuple[str, str]] = []

    with open(filename, encoding=UTF_8) as file:
        txt_data = file.read()
        matches = list(re.finditer(PATTERN, txt_data))
        matches.reverse()
        index = -1

        for match in matches:
            data.append((match.group(1), clear_text(txt_data[match.end():index])))
            index = match.start()

    save_df_to_csv_and_arff(
        pd.DataFrame(data, columns=["title", "content"]),
        get_filename_from_path(filename), False
    )


def clear_text(text: str) -> str:
    return " ".join(text.translate(
        str.maketrans(PUNCTUATION_CHARACTERS, " " * len(PUNCTUATION_CHARACTERS))
    ).lower().split())


def save_df_to_csv_and_arff(df: pd.DataFrame, filename: str, add_date: bool = True) -> None:
    df.to_csv(OUTPUT_DIR + prepare_filename(filename, CSV, add_date), index=False)
    arff.dump(
        OUTPUT_DIR + prepare_filename(filename, ARFF, add_date), df.values,
        relation=filename, names=df.columns
    )


def get_filename_from_path(filepath: str) -> str:
    return os.path.splitext(os.path.basename(filepath))[0]


def prepare_filename(name: str, extension: str, add_date: bool = True) -> str:
    return (name + ("-" + datetime.now().strftime("%H%M%S") if add_date else "")
            + extension).replace(" ", "")


def prepare_args() -> Namespace:
    arg_parser = ArgumentParser()

    arg_parser.add_argument(
        "-f", "--filepath", required=True, type=str, help="HTML or plain text filepath"
    )
    arg_parser.add_argument(
        "--plain", default=False, action="store_true", help="Convert HTML to plain text"
    )
    arg_parser.add_argument(
        "--arff", default=False, action="store_true", help="Convert plain text to arff"
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
