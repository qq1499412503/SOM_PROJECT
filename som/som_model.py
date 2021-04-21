import math
import numpy as np
import pandas as pa
import csv
from minisom import MiniSom

#
#
# for centroid in som.get_weights():
#     plt.scatter(centroid[:, 0], centroid[:, 1], marker='x',
#                 s=0.8, linewidths=3, color='k', label='centroid')


def load_data(url):
    data = np.loadtxt(url, skiprows=1)
    return data


def print_attribute(url):
    df = load_data(url)
    return df.shape[1], df.shape[0]


class Som:

    def __init__(self):
        self.data = None
        self.model_som = None
        self.x = None
        self.y = None
        self.input_len = None
        self.sigma = 0.3
        self.lr = 0.5
        self.neighborhood_function = 'gaussian'
        self.topology = 'rectangular'
        self.activation_distance = 'euclidean'
        self.random_seed = None
        self.weights = None

    def read_data(self, raw_data):
        self.data = np.array(raw_data)

    def load_length(self):
        self.input_len = self.data.shape[1]

    def model(self):
        if self.random_seed is not None:
            self.model_som = MiniSom(x=self.x, y=self.y, input_len=self.input_len, sigma=self.sigma, learning_rate=self.lr,
                                     neighborhood_function=self.neighborhood_function,topology=self.topology,
                                     activation_distance=self.activation_distance,random_seed=self.random_seed)
        else:
            self.model_som = MiniSom(x=self.x, y=self.y, input_len=self.input_len, sigma=self.sigma,
                                     learning_rate=self.lr,
                                     neighborhood_function=self.neighborhood_function, topology=self.topology,
                                     activation_distance=self.activation_distance)
        self.weights = self.model_som.get_weights()

    def fit(self, epoch):
        self.model_som.train(self.data, epoch)

    def process_map(self):
        coordinates = np.array([self.model_som.winner(x) for x in self.data]).T
        cluster_index = np.ravel_multi_index(coordinates, (self.x, self.y))
        num_ind = 1
        map = {}
        node_list = []
        print(np.unique(cluster_index))
        color = ['red', 'blue', 'yellow', 'green', '#7AB415', '#1DD676']
        for index in np.unique(cluster_index):
            # print(index)
            x = self.data[cluster_index == index, 0]
            y = self.data[cluster_index == index, 1]
            # print(len(x))
            for sub_index in range(len(x)):
                nodes = {'id': str(num_ind)+str(sub_index), 'label': str(index), 'x': round(float(x[sub_index]),2), 'y': round(float(y[sub_index]),2),
                         'size': 2, 'color': color[num_ind-1], 'class': str(num_ind)}
                # print(nodes)
                node_list.append(nodes)
            num_ind += 1

        cp_count = 0
        # for cp in self.weights:
        #     nodes = {'id': str('cp') + str(cp_count), 'label': str(cp_count), 'x': round(float(cp[:, 0][0]), 2),
        #              'y': round(float(cp[:, 1][0]), 2),
        #              'size': 2, 'color': 'black', 'class': str(cp_count)}
        #     node_list.append(nodes)
        #     cp_count+=1

        #nodes center point
        map['nodes'] = node_list
        return map
