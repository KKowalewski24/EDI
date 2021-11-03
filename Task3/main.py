import os
import random
import subprocess
import sys
from argparse import ArgumentParser, Namespace
from datetime import datetime
from typing import List, Tuple

import numpy as np
import pandas as pd
from sklearn.metrics import jaccard_score

"""
    How to run:
        python main.py -f data/clusters4.csv
        python main.py -f data/clusters4.csv -ru
    
"""

# VAR ------------------------------------------------------------------------ #
OUTPUT_DIR: str = "output/"

CONSTANT_USER: List[bool] = [
    False, False, True, False, False, False, False, True, False, False, False, True, False, False,
    True, False, False, True, True, False, True, True, False, True, False, True, False, False, False,
    False, False, False, True, False, False, True
]


# MAIN ----------------------------------------------------------------------- #
def main() -> None:
    args = prepare_args()
    filepath = args.filepath
    is_random_user = args.random_user

    print("Loading data ...")
    clusters, pages = load_clusters_and_pages(filepath)

    if len(CONSTANT_USER) != len(pages) and not is_random_user:
        print("Number of pages and visited pages by user must be equal, "
              "otherwise program cannot work !!!")
        return

    print("Preparing user ...")
    user: List[bool] = get_user(is_random_user, len(pages))

    print("Calculating similarities ...")
    similarities, most_similar_cluster_index = calculate_similarities(clusters, user)

    display_finish()


# DEF ------------------------------------------------------------------------ #
def load_clusters_and_pages(filepath: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    df = pd.read_csv(filepath, header=None, delim_whitespace=True)
    clusters = df.iloc[:, 2:]
    pages = df.iloc[:, 0]
    return clusters, pages


def get_user(is_random_user: bool, random_user_pages_number: int) -> List[bool]:
    if is_random_user:
        return [random.choice([True, False]) for _ in range(random_user_pages_number)]

    return CONSTANT_USER


def calculate_similarities(clusters: pd.DataFrame, user: List[bool]) -> Tuple[List[List], int]:
    similarities: List[List] = [
        [index, jaccard_score(user, clusters[name].to_numpy())]
        for index, name in enumerate(clusters.columns)
    ]
    most_similar_cluster_index = np.argmax(similarities, axis=0)[1]

    return similarities, most_similar_cluster_index


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
