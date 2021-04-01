import math
import numpy as np
from minison import MiniSom

winner_coordinates = np.array([som.winner(x) for x in data]).T

cluster_index = np.ravel_multi_index(winner_coordinates, (1,2))
print(cluster_index)
import matplotlib.pyplot as plt
som.win_map(data,return_indices=True)
# for a in range(8):
#     print(som.winner(data[a]))

for c in np.unique(cluster_index):
    plt.scatter(data[cluster_index == c, 0],
                data[cluster_index == c, 1], label='cluster='+str(c), alpha=.7)

for centroid in som.get_weights():
    plt.scatter(centroid[:, 0], centroid[:, 1], marker='x',
                s=0.8, linewidths=3, color='k', label='centroid')
plt.legend();


class Som:

    def __init__(self):
        self.data = None
        self.model_som = None
        self.x = 1
        self.y = 2



    def read_data(self, raw_data):
        self.data = np.array(raw_data)

    def model(self, x, y, sigma=0.3, learning_rate=0.5):
        self.x = x
        self.y = y
        self.model_som = MiniSom(self.x, self.y, self.data.shape[1], sigma=sigma, learning_rate=learning_rate)

    def fit(self, epoch):
        self.model_som.train(self.data, epoch)

    def process_map(self):
        coordinates = np.array([self.model_som.winner(x) for x in self.data]).T
        cluster_index = np.ravel_multi_index(coordinates, (1, 2))
