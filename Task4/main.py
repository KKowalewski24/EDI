import glob
from argparse import ArgumentParser, Namespace

from sklearn.neural_network import MLPRegressor

from module.ImagePostprocessor import ImagePostprocessor
from module.ImagePreprocessor import ImagePreprocessor
from module.constants import DATA_DIR, IMAGE_WIDTH, RESULTS_DIR
from module.utils import create_directory, display_finish, run_main

"""
    How to run:
        python main.py -n 2 4 6 8 10 12 20 30 -i 10000 -lr 0.01 -pn 10000 -pw 8 -ti data/01.bmp data/03.bmp
"""


def main() -> None:
    args = prepare_args()
    neurons_sequence = args.neurons_sequence
    iterations = args.iterations
    learning_rate = args.learning_rate
    patterns_number = args.patterns_number
    pattern_width = args.pattern_width
    training_image_paths = args.training_images
    create_directory(RESULTS_DIR)

    test_image_paths = [
        image_path for image_path in [path.replace("\\", "/") for path in glob.glob(f"{DATA_DIR}*")]
        if image_path not in training_image_paths
    ]

    image_preprocessor: ImagePreprocessor = ImagePreprocessor(
        training_image_paths, test_image_paths, patterns_number, pattern_width, IMAGE_WIDTH
    )

    training_images_array = image_preprocessor.preprocess_training_images()
    test_images_array = image_preprocessor.preprocess_test_images()

    for neurons in neurons_sequence:
        mlp = MLPRegressor(
            hidden_layer_sizes=neurons, max_iter=iterations,
            learning_rate_init=learning_rate, solver='sgd',
            activation='identity', alpha=0, momentum=0
        )
        mlp.fit(training_images_array, training_images_array)
        compressed_images_array = [mlp.predict(test_image) for test_image in test_images_array]

        for test_image, compressed_image in zip(test_images_array, compressed_images_array):
            image_postprocessor: ImagePostprocessor = ImagePostprocessor(
                compressed_image, pattern_width, IMAGE_WIDTH
            )
            image_postprocessor.convert_to_image()
            image_postprocessor.save_image()

    display_finish()


def prepare_args() -> Namespace:
    arg_parser = ArgumentParser()

    arg_parser.add_argument(
        "-n", "--neurons_sequence", type=int, nargs="+", required=True,
        help="List of number of neurons in hidden layers"
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
