from typing import List

import numpy as np
from sklearn.neural_network import MLPRegressor
from tqdm import tqdm


class AutoCoder:

    def __init__(self, training_images_array: List[float], test_images_array: List[List[float]],
                 neurons: int, iterations: int, learning_rate: float) -> None:
        self.training_images_array = training_images_array
        self.test_images_array = test_images_array
        self.neurons = neurons
        self.iterations = iterations
        self.learning_rate = learning_rate


    def compress_images(self) -> List[np.ndarray]:
        mlp = MLPRegressor(
            hidden_layer_sizes=self.neurons, max_iter=self.iterations,
            learning_rate_init=self.learning_rate, solver='sgd',
            activation='identity', alpha=0, momentum=0
        )

        mlp.fit(self.training_images_array, self.training_images_array)
        return [mlp.predict(test_image) for test_image in tqdm(self.test_images_array)]
