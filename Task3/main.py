import random
import subprocess
import sys
from argparse import ArgumentParser, Namespace
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
    False, False, False, False, False, False, True, False, True, True, False, False, True, True,
    True, True, True, False, False, False, True, True, False, False, True, False, False, True,
    True, False, False, False, False, True, True, False
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
    (
        similarities, most_similar_cluster_index,
        most_similar_cluster_coefficient_value
    ) = calculate_similarities(clusters, user)

    print("\nCalculated similarities:")
    for similarity in similarities:
        print("Index: ", similarity[0], "Value: ", round(similarity[1], 4))

    print(
        "Jaccard similarity coefficient value for most similar cluster:",
        round(most_similar_cluster_coefficient_value, 4), end="\n\n"
    )

    print("Recommended pages:")
    recommended_pages = get_recommended_pages(clusters, pages, user, most_similar_cluster_index)

    if len(recommended_pages) == 0:
        print("Lack of recommended pages, try again for different data!")
        return

    for recommended_page in recommended_pages:
        print(recommended_page)

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


def calculate_similarities(clusters: pd.DataFrame,
                           user: List[bool]) -> Tuple[List[List], int, float]:
    similarities: List[List] = [
        [index, jaccard_score(user, clusters[name].to_numpy())]
        for index, name in enumerate(clusters.columns)
    ]

    most_similar_cluster_index = np.argmax(similarities, axis=0)[1]
    most_similar_cluster_coefficient_value = similarities[most_similar_cluster_index][1]

    return similarities, most_similar_cluster_index, most_similar_cluster_coefficient_value


def get_recommended_pages(clusters: pd.DataFrame, pages: pd.DataFrame,
                          user: List[bool], most_similar_cluster_index: int) -> List[str]:
    most_similar_flags = clusters[clusters.columns[most_similar_cluster_index]].to_numpy()
    return [
        pages.iloc[index] for index in range(len(user))
        if not user[index] and most_similar_flags[index]
    ]


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
