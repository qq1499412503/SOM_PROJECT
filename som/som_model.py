import math
import numpy as np
import pandas as pa
import csv
from minisom import MiniSom
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon, Ellipse
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import cm, colorbar
from matplotlib.lines import Line2D
import matplotlib
from bokeh.colors import RGB
from bokeh.io import curdoc, show, output_notebook
from bokeh.transform import factor_mark, factor_cmap
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure, output_file

#
#
# for centroid in som.get_weights():
#     plt.scatter(centroid[:, 0], centroid[:, 1], marker='x',
#                 s=0.8, linewidths=3, color='k', label='centroid')


def load_data(url):
    try:
        data = np.loadtxt(url, skiprows=1)
        return data, None
    except:
        rdata = np.loadtxt(url, skiprows=1, dtype=str)
        label = rdata[:, -1]
        data = rdata[:, :-1]
        data = data.astype(np.float)
        return data, label


def print_attribute(url):
    df,_ = load_data(url)
    return df.shape[1], df.shape[0]

class Som:

    def __init__(self):
        self.data = None
        self.label = None
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

    def read_label(self, raw_label):
        self.label = raw_label

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
        map={}
        nodes = []
        weight = []
        xx, yy = self.model_som.get_euclidean_coordinates()
        umatrix = self.model_som.distance_map()
        weights = self.model_som.get_weights()
        for j in range(weights.shape[1]):
            sub_nodes = []
            sub_weight = []
            for i in range(weights.shape[0]):
                color = matplotlib.colors.rgb2hex(cm.Blues(umatrix[i, j]))
                sub_nodes.append(color)
                weight_raw = weights[i,j].tolist()
                weight_process = ""
                for w in weight_raw:
                    weight_process = weight_process + str(w) + ' '
                sub_weight.append(weight_process)
            nodes.append(sub_nodes)
            weight.append(sub_weight)
        map['nodes'] = nodes
        map['weights'] = weight
        # print(map)
        d_count = 0
        x_winner = [' ' for a in range(self.x)]
        main_winner = [x_winner for b in range(self.y)]
        if self.label is not None:
            for each_data in self.data:
                winner = self.model_som.winner(each_data)
                sub_str = main_winner[winner[0]][winner[1]] + str(self.label[d_count])
                sub_list = [' ' for a in range(self.x)]
                sub_list[winner[1]] = sub_str
                main_winner[winner[0]] = sub_list
                main_winner[winner[0]][winner[1]] += ' '
                d_count += 1
            map['label'] = main_winner
            print(main_winner)
        return map




