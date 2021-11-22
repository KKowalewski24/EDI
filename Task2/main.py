import os
import subprocess
import sys
from argparse import ArgumentParser, Namespace
from datetime import datetime

import arff
import html2text
import pandas as pd
from tqdm import tqdm

"""
    How to run:
        python main.py -f data/ftims.html --plain
        python main.py -f output/ftims.txt --arff
"""

# VAR ------------------------------------------------------------------------ #
UTF_8: str = "utf-8"
OUTPUT_DIR: str = "output/"
CSV: str = ".csv"
ARFF: str = ".arff"
TXT: str = ".txt"
TERM = "Page "


# MAIN ----------------------------------------------------------------------- #
def main() -> None:
    args = prepare_args()
    create_directory(OUTPUT_DIR)
    filepath = args.filepath
    to_plain = args.plain
    to_arff = args.arff

    if to_plain:
        convert_html_to_plain(filepath)
    elif to_arff:
        convert_plain_text_to_arff(filepath)

    display_finish()


# DEF ------------------------------------------------------------------------ #
def convert_html_to_plain(filepath: str) -> None:
    with open(filepath) as file:
        plain_text = html2text.html2text(file.read())

    with open(OUTPUT_DIR + get_filename_from_path(filepath) + TXT, "w", encoding=UTF_8) as file:
        file.write(plain_text)


def convert_plain_text_to_arff(filepath: str) -> None:
    df = pd.DataFrame(columns=["title", "content"])
    page_counter = 0
    line_back = ""
    title = ""
    content = ""

    with open(filepath, encoding=UTF_8) as file:
        for line in tqdm(file):
            line.strip().split("/n")
            if TERM in line:
                if title != "":
                    title = TERM + str(page_counter)
                    page_counter += 1
                    df.loc[-1] = [title, content]
                    df.index = df.index + 1
                    df = df.sort_index()
                result = line.partition("[")[2].partition("]")[0]
                if result == "":
                    result = line_back.partition("[")[2].partition("]")[0]
                title = result
                content = ""
            else:
                content += line
            line_back = line

    df = df[::-1]
    save_df_to_csv_and_arff(df, get_filename_from_path(filepath), False)


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


def create_directory(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)


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
