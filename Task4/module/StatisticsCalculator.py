import math
from typing import List

import matplotlib.pyplot as plt
import numpy as np


class StatisticsCalculator:
    BITS_IN_BYTE = 8
    BITS_TO_REMEMBER_HIDDEN_FACTOR = 12
    BITS_TO_REMEMBER_WEIGHT = 8


    def __init__(self, pattern_width: int, image_width: int, test_image_names: List[str]) -> None:
        self.pattern_width = pattern_width
        self.image_width = image_width
        self.stats = {}
        for test_image_name in test_image_names:
            self.stats[test_image_name] = {}


    def calculate_stats(self, test_image_array: List[float],
                        compressed_image_array: np.ndarray,
                        neurons: int, image_name: str) -> None:
        compression_ratio = self._calculate_compression_ratio(neurons)
        psnr = self._calculate_psnr(test_image_array, compressed_image_array)
        self.stats[image_name][compression_ratio] = psnr


    def plot_statistics(self, title: str, filepath: str) -> None:
        for name, stat in self.stats.items():
            plt.plot(stat.keys(), stat.values(), label=name, marker="s", markersize=4)

        self._set_descriptions(title, "Compression ratio", "PSNR")
        plt.legend()
        plt.savefig(filepath)


    def _calculate_compression_ratio(self, neurons: int):
        input_output_neurones = self.pattern_width * self.pattern_width
        value = (
                input_output_neurones * neurons * StatisticsCalculator.BITS_TO_REMEMBER_WEIGHT +
                neurons * StatisticsCalculator.BITS_TO_REMEMBER_HIDDEN_FACTOR +
                neurons * input_output_neurones * StatisticsCalculator.BITS_TO_REMEMBER_WEIGHT
        )
        return (StatisticsCalculator.BITS_IN_BYTE * self.image_width * self.image_width) / value


    def _calculate_psnr(self, test_image_array: List[float], compressed_image_array: np.ndarray):
        test_image_ravelled = np.array(test_image_array).ravel()
        compressed_image_ravelled = np.array(compressed_image_array).ravel()

        if len(test_image_ravelled) != len(compressed_image_ravelled):
            raise Exception("Images must have equal size!")

        image_sum = 0
        for test_image, compressed_image in zip(test_image_ravelled, compressed_image_ravelled):
            image_sum += math.pow((test_image - compressed_image) * 255, 2)

        return 10 * math.log10((255 * 255) / (image_sum / (self.image_width * self.image_width)))


    def _set_descriptions(self, title: str, x_label: str = "", y_label: str = "") -> None:
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
