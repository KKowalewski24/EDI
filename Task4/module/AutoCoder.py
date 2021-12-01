from typing import List

from sklearn.neural_network import MLPRegressor


class AutoCoder:

    def __init__(self, training_images: List[float], test_images: List[List[float]],
                 neurons: int, iterations: int, learning_rate: float) -> None:
        self.training_images = training_images
        self.test_images = test_images
        self.neurons = neurons
        self.iterations = iterations
        self.learning_rate = learning_rate


    def compress_image(self) -> None:
        mlp = MLPRegressor(
            hidden_layer_sizes=self.neurons, max_iter=self.iterations,
            learning_rate_init=self.learning_rate, solver='sgd',
            activation='identity', alpha=0, momentum=0
        )
        mlp.fit(self.training_images, self.training_images)
