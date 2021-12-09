import math
from typing import List

import matplotlib.pyplot as plt
import numpy as np


class StatisticsCalculator:

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
        BITS_IN_BYTE = 8
        BITS_TO_REMEMBER_HIDDEN_FACTOR = 12
        BITS_TO_REMEMBER_WEIGHT = 8
        in_out_neurones = self.pattern_width * self.pattern_width
        return (BITS_IN_BYTE * self.image_width * self.image_width) / \
               (in_out_neurones * neurons * BITS_TO_REMEMBER_WEIGHT +
                neurons * BITS_TO_REMEMBER_HIDDEN_FACTOR +
                neurons * in_out_neurones * BITS_TO_REMEMBER_WEIGHT)


    def _calculate_psnr(self, test_image_array: List[float], compressed_image_array: np.ndarray):
        orginal_image = np.array(test_image_array).ravel()
        reduced_image = np.array(compressed_image_array).ravel()

        if len(orginal_image) != len(reduced_image):
            raise ValueError(f'Orginal image ({len(orginal_image)}) \
                differs in size from reduced image ({len(reduced_image)})')

        img_sum = 0
        for i in range(len(orginal_image)):
            img_sum += math.pow((orginal_image[i] - reduced_image[i]) * 255, 2)

        return 10 * math.log10((255 * 255) / (img_sum / (512 * 512)))


    def _set_descriptions(self, title: str, x_label: str = "", y_label: str = "") -> None:
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
