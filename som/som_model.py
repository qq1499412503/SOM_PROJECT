import math
import numpy as np
from minison import MiniSom

#
#
# for centroid in som.get_weights():
#     plt.scatter(centroid[:, 0], centroid[:, 1], marker='x',
#                 s=0.8, linewidths=3, color='k', label='centroid')



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
        cluster_index = np.ravel_multi_index(coordinates, (self.x, self.y))
        num_ind = 1
        map = {}
        node_list = []

        for index in np.unique(cluster_index):
            nodes = {'id': str(num_ind), 'label':str(index), 'x': self.data[cluster_index == index, 0], 'y': self.data[cluster_index == index, 1],
                     'size': 2, 'color': '#17202A'}
            num_ind += 1
            node_list.append(nodes)

        #nodes center point
        map['nodes'] = node_list
        return map
