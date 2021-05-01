import math
import numpy as np
from minison import MiniSom


data = [[ 0.80,  0.55,  0.22,  0.03],
        [ 0.82,  0.50,  0.23,  0.03],
        [ 0.80,  0.54,  0.22,  0.03],
        [ 0.80,  0.53,  0.26,  0.03],
        [ 0.79,  0.56,  0.22,  0.03],
        [ 0.75,  0.60,  0.25,  0.03],
        [ 0.77,  0.59,  0.22,  0.03],
        [0.1,0.2,0.3,0.01]]
data = np.array(data)

som = MiniSom(1, 2, 4, sigma=0.3, learning_rate=0.5) # initialization of 6x6 SOM
som.train(data, 100) # trains the SOM with 100 iterations

# som.winner(data[0])



class sommodel():

    def __init__(self):
        pass

    def model(self):
        som = MiniSom(1, 2, 4, sigma=0.3, learning_rate=0.5)