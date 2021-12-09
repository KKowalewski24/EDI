from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np


class StatisticsCalculator:

    def __init__(self, pattern_width: int, image_width: int) -> None:
        self.pattern_width = pattern_width
        self.image_width = image_width
        self.stats: List[Tuple[str, float, float]] = []


    def calculate_stats(self, test_image_array: List[float],
                        compressed_image_array: np.ndarray,
                        neurons: int, image_name: str) -> None:
        self.stats.append((
            image_name,
            self._calculate_compression_ratio(neurons),
            self._calculate_psnr(test_image_array, compressed_image_array)
        ))


    def plot_statistics(self, title: str, filepath: str) -> None:
        for stat in self.stats:
            name, compression_ratio, psnr = stat
            # plt.plot(compression_ratio, psnr, label=name, marker="s", markersize=4)

        self._set_descriptions(title, "Compression ratio", "PSNR")
        plt.legend()
        plt.savefig(filepath)


    def _calculate_compression_ratio(self, neurons: int):
        pass


    def _calculate_psnr(self, test_image_array: List[float], compressed_image_array: np.ndarray):
        pass


    def _set_descriptions(self, title: str, x_label: str = "", y_label: str = "") -> None:
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
