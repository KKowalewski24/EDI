import glob
from argparse import ArgumentParser, Namespace

from module.AutoCoder import AutoCoder
from module.ImagePreprocessor import ImagePreprocessor
from module.StatisticsCalculator import StatisticsCalculator
from module.utils import create_directory, display_finish, run_main

"""
    How to run:
        python main.py -n 2 4 6 8 10 12 20 30 -i 10000 -lr 0.01 -pn 10000 -pw 8 -ti data/01.bmp data/03.bmp
"""

# VAR ------------------------------------------------------------------------ #
RESULTS_DIR = "results/"
DATA_DIR = "data/"


# MAIN ----------------------------------------------------------------------- #
def main() -> None:
    args = prepare_args()
    neurons = args.neurons
    iterations = args.iterations
    learning_rate = args.learning_rate
    patterns_number = args.patterns_number
    pattern_width = args.pattern_width
    training_image_paths = args.training_images
    create_directory(RESULTS_DIR)

    test_image_paths = [
        image_path for image_path in glob.glob(f"{DATA_DIR}*")
        if image_path not in training_image_paths
    ]

    image_preprocessor: ImagePreprocessor = ImagePreprocessor(
        training_image_paths, test_image_paths, patterns_number, pattern_width
    )
    image_preprocessor.preprocess_training_images()
    statistics_calculator: StatisticsCalculator = StatisticsCalculator()
    auto_coder: AutoCoder = AutoCoder()

    display_finish()


# DEF ------------------------------------------------------------------------ #
def prepare_args() -> Namespace:
    arg_parser = ArgumentParser()

    arg_parser.add_argument(
        "-n", "--neurons", type=int, nargs="+", required=True,
        help="Number of neurons in hidden layers"
    )
    arg_parser.add_argument(
        "-i", "--iterations", type=int, required=True,
        help="Number of MLP iterations"
    )
    arg_parser.add_argument(
        "-lr", "--learning_rate", type=float, required=True,
        help="Number of MLP iterations"
    )
    arg_parser.add_argument(
        "-pn", "--patterns_number", type=int, required=True,
        help="Number of patterns, big numbers give best results"
    )
    arg_parser.add_argument(
        "-pw", "--pattern_width", type=int, required=True,
        help="Pattern width"
    )
    arg_parser.add_argument(
        "-ti", "--training_images", type=str, nargs="+", required=True,
        help=f"Paths to training images, rest of images are taken from {DATA_DIR} directory!"
    )

    return arg_parser.parse_args()


# __MAIN__ ------------------------------------------------------------------- #
if __name__ == "__main__":
    run_main(main)
