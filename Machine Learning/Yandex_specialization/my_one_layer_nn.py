import numpy as np
import pandas as pd
from scipy.special import expit
from sklearn.datasets import make_moons
from sklearn.metrics import (accuracy_score, roc_auc_score)
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

RANDOM_STATE = 1
np.random.seed(RANDOM_STATE)


class SingleLayerParams:
    def __init__(self,
                 n_neurons: int,
                 n_features: int,
                 random_state: int = RANDOM_STATE):
        """
            The main idea in hidden layers: 
            size_x - number of "features" in previous layer 
                - by features I mean that if hidden layer has 4 nodes - it means that from
                - initial 10 features this matrix would give us 4 new features - which 
                - become an input for the next output layer
            size_y - number of neurons on the output layer
        """
        self.size_y = n_neurons
        self.size_x = n_features

        self.weight = np.random.randn(self.size_y, self.size_x) * 0.01
        self.bias = np.zeros((n_neurons, 1))


class SingleLayerClassificationNN:
    def __init__(self,
                 n_hidden: int = 4,
                 learinig_rate=1.2,
                 max_iter: int = 10000,
                 random_state: int = RANDOM_STATE):
        self.n_h = n_hidden
        self.lr = learinig_rate
        self.max_iter = max_iter
        self.random_state = random_state
        self.threshold = 0.5

        # NN dimentions
        self.n_inp = None
        self.n_out = None

        # Hidden layers & activation functions
        self.layers = [None, None]
        self.act_func = [lambda x: np.tanh(x), lambda x: expit(x)]
        self.act_grads = [
            lambda x: 1. - np.tanh(x)**2, lambda x: expit(x) * (1. - expit(x))
        ]

    def __set_dimentions(self, X_train: np.array, y_train: np.array):
        (n_features, n_samples0) = X_train.shape
        (n_outputs, n_samples1) = y_train.shape

        if n_samples0 != n_samples1:
            raise Exception('Number of samples for trinig is different')

        return n_features, n_outputs, n_samples0

    def __initialize_weights(self):
        self.layers[0] = SingleLayerParams(self.n_h, self.n_inp)
        self.layers[1] = SingleLayerParams(self.n_out, self.n_h)

    def __forward_propagation(self, X: np.array) -> np.array:
        res = dict()
        res['Z1'] = self.layers[0].weight.dot(X) + self.layers[0].bias
        res['A1'] = self.act_func[0](res['Z1'])
        res['Z2'] = self.layers[1].weight.dot(res['A1']) + self.layers[1].bias
        res['A2'] = self.act_func[1](res['Z2'])
        return res

    def __compute_loss(self, A2: np.array, y_train: np.array,
                       n_obj: int) -> float:
        log_loss = y_train * np.log(A2) + (1. - y_train) * np.log(1. - A2)
        return -np.sum(log_loss) / n_obj

    def __backward_propagation(self, outputs: list, X: np.array,
                               y_train: np.array, n_obj: int) -> list:
        grads = [None for _ in range(len(self.layers))]
        # Start with te last layer
        layer_id = len(self.layers) - 1

        # Back propogation for last layer
        dZ2 = outputs['A2'] - y_train
        grads[layer_id] = {
            'dW': dZ2.dot(outputs['A1'].T) / n_obj,
            'db': np.sum(dZ2, axis=1, keepdims=True)
        }
        layer_id -= 1

        # Back propogation for first layer
        dZ1 = self.layers[1].weight.T.dot(dZ2) * self.act_grads[0](
            outputs['Z1'])
        grads[layer_id] = {
            'dW': dZ1.dot(X.T) / n_obj,
            'db': np.sum(dZ1, axis=1, keepdims=True)
        }

        return grads

    def __update_weights(self, grads: list):
        for ID, layer in enumerate(self.layers):
            layer.weight = layer.weight - self.lr * grads[ID]['dW']
            layer.bias = layer.bias - self.lr * grads[ID]['db']

    def fit(self, X_train: np.array, y_train: np.array):
        self.n_inp, self.n_out, n_obj = self.__set_dimentions(X_train, y_train)
        self.__initialize_weights()

        loss = 0.
        for ID in range(self.max_iter):
            outputs = self.__forward_propagation(X_train)
            loss = self.__compute_loss(outputs['A2'], y_train, n_obj)
            if ID % 1000 == 0:
                print(f'{ID}: loss = {loss}')
            grads = self.__backward_propagation(outputs, X_train, y_train,
                                                n_obj)
            self.__update_weights(grads)

    def predict(self, X_test: np.array) -> np.array:
        res = self.__forward_propagation(X_test)['A2']
        return res > self.threshold


def plot_decision_boundary(model, X, y):
    # Set min and max values and give it some padding
    x_min, x_max = X[0, :].min() - 1, X[0, :].max() + 1
    y_min, y_max = X[1, :].min() - 1, X[1, :].max() + 1
    h = 0.01
    # Generate a grid of points with distance h between them
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    # Predict the function value for the whole grid
    Z = model(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    # Plot the contour and training examples
    plt.contourf(xx, yy, Z, cmap=plt.cm.Spectral)
    plt.ylabel('x2')
    plt.xlabel('x1')
    plt.scatter(X[0, :], X[1, :], c=y, cmap=plt.cm.Spectral)


if __name__ == "__main__":
    clf = SingleLayerClassificationNN(n_hidden=4, learinig_rate=0.05)
    X, y = make_moons(random_state=1, noise=0.3)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, train_size=0.65, random_state=RANDOM_STATE)

    clf.fit(X_train.T, y_train[:, np.newaxis].T)

    fig = plt.figure(figsize=(9, 8))
    ax = plt.subplot(221)
    ax.scatter(X_train[:, 0], X_train[:, 1], c=y_train, s=50, edgecolor='k')
    plot_decision_boundary(lambda x: clf.predict(x.T), X_train.T, y_train)

    y_pred = clf.predict(X_test.T)

    print(f'Accuracy: {accuracy_score(y_test, y_pred.T)}')
    print(f'AUC ROC: {roc_auc_score(y_test, y_pred.T)}')

    plt.show()