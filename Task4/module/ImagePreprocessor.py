from typing import List

import numpy as np
from PIL import Image


class ImagePreprocessor:

    def __init__(self, training_image_paths: List[str], test_image_paths: List[str],
                 patterns_number: int, pattern_width: int, image_width: int) -> None:
        self.training_image_paths = training_image_paths
        self.test_image_paths = test_image_paths
        self.patterns_number = patterns_number
        self.pattern_width = pattern_width
        self.image_width = image_width


    def preprocess_training_images(self) -> List[float]:
        images_array: List[float] = []
        for image_path in self.training_image_paths:
            images_array += self._prepare_random_patterns(self._read_and_rescale(image_path))

        return images_array


    def preprocess_test_images(self) -> List[List[float]]:
        images_array: List[List[float]] = []
        for image_path in self.test_image_paths:
            images_array.append(self._prepare_all_patterns(self._read_and_rescale(image_path)))

        return images_array


    def _prepare_random_patterns(self, image: List) -> List:
        patterns = []
        patterns_indexes = []
        self._check_pattern_ratio()

        while len(patterns) < self.patterns_number:
            row_index = np.random.randint(0, self.image_width - self.pattern_width + 1)
            col_index = np.random.randint(0, self.image_width - self.pattern_width + 1)

            if [row_index, col_index] not in patterns_indexes:
                patterns_indexes.append([row_index, col_index])
                pattern = image[
                          row_index: row_index + self.pattern_width,
                          col_index: col_index + self.pattern_width
                          ]
                patterns.append(pattern.ravel())

        return patterns


    def _prepare_all_patterns(self, image: List) -> List:
        patterns = []
        self._check_pattern_ratio()

        row = 0
        while row < self.image_width:
            col = 0
            while col < self.image_width:
                pattern = image[row: row + self.pattern_width, col: col + self.pattern_width]
                patterns.append(pattern.ravel())
                col += self.pattern_width
            row += self.pattern_width

        return patterns


    def _check_pattern_ratio(self) -> None:
        image_pattern_ratio = self.image_width / self.pattern_width
        if not image_pattern_ratio.is_integer():
            raise Exception("Result of dividing image_width AND pattern_width should be an integer!")


    def _read_and_rescale(self, image_path: str) -> List:
        return np.asarray(Image.open(image_path)) / 255 * 2 - 1
