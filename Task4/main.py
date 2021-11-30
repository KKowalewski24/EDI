from argparse import ArgumentParser, Namespace

from module.utils import display_finish, run_main, create_directory

"""
    How to run:
        python main.py -n 2 4 6 8 10 12 20 30 -i 10000 -lr 0.01 -pn 10000 -pw 8 -ti data/01.bmp data/03.bmp
"""

# VAR ------------------------------------------------------------------------ #
RESULTS_DIR = "results/"


# MAIN ----------------------------------------------------------------------- #
def main() -> None:
    args = prepare_args()
    neurons = args.neurons
    iterations = args.iterations
    learning_rate = args.learning_rate
    patterns_number = args.patterns_number
    pattern_width = args.pattern_width
    training_images = args.training_images
    create_directory(RESULTS_DIR)

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
        help="Paths to training images, rest of images from this directory is for testing!"
    )

    return arg_parser.parse_args()


# __MAIN__ ------------------------------------------------------------------- #
if __name__ == "__main__":
    run_main(main)
