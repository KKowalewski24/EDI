from typing import List

import numpy as np
from PIL import Image


class ImagePostprocessor:

    def __init__(self, compressed_image_array: List[np.ndarray],
                 pattern_width: int, image_width: int) -> None:
        self.compressed_image_array = compressed_image_array
        self.pattern_width = pattern_width
        self.image_width = image_width
        self.compressed_image = None


    def convert_to_image(self) -> None:
        patterns_in_row = int(self.image_width / self.pattern_width)
        image_reshaped = [
            pattern.reshape(self.pattern_width, self.pattern_width)
            for pattern in self.compressed_image_array
        ]

        global_rows = []
        for i in range(patterns_in_row):
            rows = []
            for _ in range(self.pattern_width):
                rows.append([])

            for j in range(patterns_in_row):
                for k in range(self.pattern_width):
                    rows[k] += image_reshaped[i * patterns_in_row + j][k].tolist()

            global_rows += rows

        self.compressed_image = Image.fromarray(self._rescale_to_px(np.array(global_rows)))


    def save_image(self) -> None:
        pass


    def _rescale_to_px(self, image_array: np.ndarray):
        return (np.clip(image_array, -1, 1) + 1) * 255 / 2
