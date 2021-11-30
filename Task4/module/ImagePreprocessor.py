from typing import List, Tuple

import numpy as np
from PIL import Image


class ImagePreprocessor:

    def __init__(self, training_image_paths: List[str], test_image_paths: List[str],
                 patterns_number: int, pattern_width: int) -> None:
        self.training_image_paths = training_image_paths
        self.test_image_paths = test_image_paths
        self.patterns_number = patterns_number
        self.pattern_width = pattern_width


    def preprocess_training_images(self) -> Tuple[List, int]:
        data = []
        image_width = 0

        for image_path in self.training_image_paths:
            if image_width == 0:
                image_width = len(np.asarray(Image.open(image_path)))

            image = self._read_and_rescale(image_path)

        return data, image_width


    def preprocess_test_images(self) -> List:
        data = []
        for image_path in self.test_image_paths:
            image = self._read_and_rescale(image_path)

        return data


    def _read_and_rescale(self, image_path: str) -> List:
        return np.asarray(Image.open(image_path)) / 255 * 2 - 1
