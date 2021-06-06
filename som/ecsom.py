from minisom import *
import numpy as np

class Mm(MiniSom):
  def __init__(self, x, y, input_len, sigma=1.0, learning_rate=0.5,
                decay_function=asymptotic_decay,
                neighborhood_function='gaussian', topology='rectangular',
                activation_distance='euclidean', random_seed=None):
      if sigma >= x or sigma >= y:
          warn('Warning: sigma is too high for the dimension of the map.')

      self._random_generator = random.RandomState(random_seed)

      self._learning_rate = learning_rate
      self._sigma = sigma
      self._input_len = input_len
      # random initialization
      self._weights = self._random_generator.rand(x, y, input_len)*2-1
      self._weights /= linalg.norm(self._weights, axis=-1, keepdims=True)

      self._activation_map = zeros((x, y))
      self._neigx = arange(3*x)
      self._neigy = arange(3*y)  # used to evaluate the neighborhood function

      if topology not in ['hexagonal', 'rectangular']:
          msg = '%s not supported only hexagonal and rectangular available'
          raise ValueError(msg % topology)
      self.topology = topology
      self._xx, self._yy = meshgrid(self._neigx, self._neigy)
      self._xx = self._xx.astype(float)
      self._yy = self._yy.astype(float)
      if topology == 'hexagonal':
          self._xx[::-2] -= 0.5
          if neighborhood_function in ['triangle']:
              warn('triangle neighborhood function does not ' +
                    'take in account hexagonal topology')

      self._decay_function = decay_function

      neig_functions = {'gaussian': self._gaussian,
                        'mexican_hat': self._mexican_hat,
                        'bubble': self._bubble,
                        'triangle': self._triangle}

      if neighborhood_function not in neig_functions:
          msg = '%s not supported. Functions available: %s'
          raise ValueError(msg % (neighborhood_function,
                                  ', '.join(neig_functions.keys())))

      if neighborhood_function in ['triangle',
                                    'bubble'] and (divmod(sigma, 1)[1] != 0
                                                  or sigma < 1):
          warn('sigma should be an integer >=1 when triangle or bubble' +
                'are used as neighborhood function')

      self.neighborhood = neig_functions[neighborhood_function]

      distance_functions = {'euclidean': self._euclidean_distance,
                            'cosine': self._cosine_distance,
                            'manhattan': self._manhattan_distance,
                            'chebyshev': self._chebyshev_distance}

      if activation_distance not in distance_functions:
          msg = '%s not supported. Distances available: %s'
          raise ValueError(msg % (activation_distance,
                                  ', '.join(distance_functions.keys())))

      self._activation_distance = distance_functions[activation_distance]


  def update(self, x, win, t, max_iteration):
    eta = self._decay_function(self._learning_rate, t, max_iteration)
    # sigma and learning rate decrease with the same rule
    sig = self._decay_function(self._sigma, t, max_iteration)
    g = self.neighborhood(win, sig)*eta
    base = x-self._weights
    bx,by,_ = base.shape
    self._weights += einsum('ij, ijk->ijk', g, np.tile(x-self._weights,(3,3,1)))[bx:bx*2,by:by*2,:]
    wx,wy = win
    g01 = self.neighborhood((wx+bx,wy), sig)*eta
    self._weights += einsum('ij, ijk->ijk', g01, np.tile(x-self._weights,(3,3,1)))[bx:bx*2,by:by*2,:]
    g02 = self.neighborhood((wx+bx*2,wy), sig)*eta
    self._weights += einsum('ij, ijk->ijk', g02, np.tile(x-self._weights,(3,3,1)))[bx:bx*2,by:by*2,:]
    g10 = self.neighborhood((wx,wy+by), sig)*eta
    self._weights += einsum('ij, ijk->ijk', g10, np.tile(x-self._weights,(3,3,1)))[bx:bx*2,by:by*2,:]
    g11 = self.neighborhood((wx+bx,wy+by), sig)*eta
    self._weights += einsum('ij, ijk->ijk', g11, np.tile(x-self._weights,(3,3,1)))[bx:bx*2,by:by*2,:]
    g12 = self.neighborhood((wx+bx*2,wy+by), sig)*eta
    self._weights += einsum('ij, ijk->ijk', g12, np.tile(x-self._weights,(3,3,1)))[bx:bx*2,by:by*2,:]
    g20 = self.neighborhood((wx,wy+by*2), sig)*eta
    self._weights += einsum('ij, ijk->ijk', g20, np.tile(x-self._weights,(3,3,1)))[bx:bx*2,by:by*2,:]
    g21 = self.neighborhood((wx+bx,wy+by*2), sig)*eta
    self._weights += einsum('ij, ijk->ijk', g21, np.tile(x-self._weights,(3,3,1)))[bx:bx*2,by:by*2,:]
    g22 = self.neighborhood((wx+bx*2,wy+by*2), sig)*eta
    self._weights += einsum('ij, ijk->ijk', g22, np.tile(x-self._weights,(3,3,1)))[bx:bx*2,by:by*2,:]

  # def distance_map(self):
  #       um = np.zeros((self._weights.shape[0]*2,
  #                   self._weights.shape[1]*2,
  #                   8))
  #       ii = [[1, 1, 1, 0, -1, 0], [0, 1, 0, -1, -1, -1]]
  #       jj = [[1, 0, -1, -1, 0, 1], [1, 0, -1, -1, 0, 1]]
  #       for x in range(self._weights.shape[0]):
  #           for y in range(self._weights.shape[1]):
  #               e = y % 2 == 0
  #               # print(e)
  #               w_2 = self._weights[x, y]
  #               new_x = 2*x
  #               new_y = 2*y
  #               # um[new_x, new_y, k] = w_2
  #               for k, (i, j) in enumerate(zip(ii[e], jj[e])):
  #
  #                   if (x+i >= 0 and x+i < self._weights.shape[0] and
  #                           y+j >= 0 and y+j < self._weights.shape[1]):
  #                       w_1 = self._weights[x+i, y+j]
  #                       um[new_x+i, new_y+j, k] = fast_norm(w_2-w_1)
  #                   elif x+i < 0 and y+j < 0:
  #                       w_1 = self._weights[self._weights.shape[0]-1, self._weights.shape[1]-1]
  #                       um[self._weights.shape[0]*2-1, self._weights.shape[1]*2-1, k] = fast_norm(w_2-w_1)
  #                       break
  #                   elif x+i < 0 and y+j < self._weights.shape[1]:
  #                       w_1 = self._weights[self._weights.shape[0]-1, y+j]
  #                       um[self._weights.shape[0]*2-1, new_y+j, k] = fast_norm(w_2-w_1)
  #                   elif y+j < 0 and x+i < self._weights.shape[0]:
  #                       w_1 = self._weights[x+i, self._weights.shape[1]-1]
  #                       um[new_x+i, self._weights.shape[1]*2-1, k] = fast_norm(w_2-w_1)
  #
  #       um = um.sum(axis=2)
  #       return um/um.max()

  def distance_map(self):
      um = np.zeros((self._weights.shape[0] * 2,
                     self._weights.shape[1] * 2))
      ii = [[1, 1, 1, 0, -1, 0], [0, 1, 0, -1, -1, -1]]
      jj = [[1, 0, -1, -1, 0, 1], [1, 0, -1, -1, 0, 1]]
      for x in range(self._weights.shape[0]):
          for y in range(self._weights.shape[1]):
              e = y % 2 == 0
              # print(e)
              w_2 = self._weights[x, y]
              new_x = 2 * x
              new_y = 2 * y
              # um[new_x, new_y, k] = w_2
              for k, (i, j) in enumerate(zip(ii[e], jj[e])):

                  if (x + i >= 0 and x + i < self._weights.shape[0] and
                          y + j >= 0 and y + j < self._weights.shape[1]):
                      w_1 = self._weights[x + i, y + j]
                      um[new_x + i, new_y + j] = fast_norm(w_2 - w_1)
                  elif x + i < 0 and y + j < 0:
                      w_1 = self._weights[self._weights.shape[0] - 1, self._weights.shape[1] - 1]
                      um[self._weights.shape[0] * 2 - 1, self._weights.shape[1] * 2 - 1] = fast_norm(w_2 - w_1)
                      # break
                  elif x + i < 0 and y + j < self._weights.shape[1]:
                      w_1 = self._weights[self._weights.shape[0] - 1, y + j]
                      um[self._weights.shape[0] * 2 - 1, new_y + j] = fast_norm(w_2 - w_1)
                  elif y + j < 0 and x + i < self._weights.shape[0]:
                      w_1 = self._weights[x + i, self._weights.shape[1] - 1]
                      um[new_x + i, self._weights.shape[1] * 2 - 1] = fast_norm(w_2 - w_1)

      return um / um.max()
  #
  # def avg_distance(self,data):
  #     for y in range(self._weights.shape[0]*2):
  #         for x in range(self._weights.shape[1]*2):
  #             if x % 2 == 0 and y % 2 == 0:
  #                 if y-1>0:
  #                     if x-1>0:
  #                         data[y,x]=(data[y,x+1]+data[y,x-1]+data[y+1,x-1]+data[y+1,x]+data[y-1,x]+data[y-1,x-1])/6
  #                     else:
  #                         data[y, x] = (data[y, x + 1] + data[y, self._weights.shape[1]] + data[y + 1, self._weights.shape[1]] + data[y + 1, x] + data[y - 1, x] + data[y - 1, self._weights.shape[1]]) / 6
  #                 else:
  #                     if x-1>0:
  #                         data[y,x]=(data[y,x+1]+data[y,x-1]+data[y+1,x-1]+data[y+1,x]+data[self._weights.shape[0],x]+data[self._weights.shape[0],x-1])/6
  #                     else:
  #                         data[y, x] = (data[y, x + 1] + data[y, self._weights.shape[1]] + data[y + 1, self._weights.shape[1]] + data[y + 1, x] + data[self._weights.shape[0], x] + data[self._weights.shape[0], self._weights.shape[1]]) / 6
  #     return data

  def avg_distance(self, data):
      od = True
      cx = 0
      for x in range(self._weights.shape[0] * 2):
          for y in range(self._weights.shape[1] * 2):
              od1 = [[x, y - 1], [x, y + 1], [x - 1, y - 1], [x - 1, y], [x + 1, y - 1], [x + 1, y]]
              od2 = [[x, y - 1], [x, y + 1], [x - 1, y], [x - 1, y + 1], [x + 1, y], [x + 1, y + 1]]
              if x % 2 == 0 and y % 2 == 0:
                  if cx != x:
                      cx = x
                      if od:
                          od = False
                      else:
                          od = True
                  if od:
                      current = od1
                      currentx = [[x, y - 1], [x, y + 1], [self._weights.shape[0] * 2 - 1, y - 1],
                                  [self._weights.shape[0] * 2 - 1, y], [x + 1, y - 1], [x + 1, y]]
                      currenty = [[x, self._weights.shape[1] * 2 - 1], [x, y + 1],
                                  [x - 1, self._weights.shape[1] * 2 - 1], [x - 1, y],
                                  [x + 1, self._weights.shape[1] * 2 - 1], [x + 1, y]]
                      currentxy = [[x, self._weights.shape[1] * 2 - 1], [x, y + 1],
                                   [self._weights.shape[0] * 2 - 1, self._weights.shape[1] * 2 - 1],
                                   [self._weights.shape[0] * 2 - 1, y], [x + 1, self._weights.shape[1] * 2 - 1],
                                   [x + 1, y]]

                  else:
                      current = od2
                      currentx = [[x, y - 1], [x, y + 1], [self._weights.shape[0] * 2 - 1, y],
                                  [self._weights.shape[0] * 2 - 1, y + 1], [x + 1, y], [x + 1, y + 1]]
                      currenty = [[x, self._weights.shape[1] * 2 - 1], [x, y + 1], [x - 1, y], [x - 1, y + 1],
                                  [x + 1, y], [x + 1, y + 1]]
                      currentxy = [[x, self._weights.shape[1] * 2 - 1], [x, y + 1], [self._weights.shape[0] * 2 - 1, y],
                                   [self._weights.shape[0] * 2 - 1, y + 1], [x + 1, y], [x + 1, y + 1]]

                  if x - 1 >= 0:
                      if y - 1 >= 0:
                          data[x, y] = (data[current[0][0], current[0][1]] + data[current[1][0], current[1][1]] + data[
                              current[2][0], current[2][1]] + data[current[3][0], current[3][1]] + data[
                                            current[4][0], current[4][1]] + data[current[5][0], current[5][1]]) / 6
                      else:

                          data[x, y] = (data[currenty[0][0], currenty[0][1]] + data[currenty[1][0], currenty[1][1]] +
                                        data[currenty[2][0], currenty[2][1]] + data[currenty[3][0], currenty[3][1]] +
                                        data[currenty[4][0], currenty[4][1]] + data[currenty[5][0], currenty[5][1]]) / 6

                  else:
                      if y - 1 > 0:
                          data[x, y] = (data[currentx[0][0], currentx[0][1]] + data[currentx[1][0], currentx[1][1]] +
                                        data[currentx[2][0], currentx[2][1]] + data[currentx[3][0], currentx[3][1]] +
                                        data[currentx[4][0], currentx[4][1]] + data[currentx[5][0], currentx[5][1]]) / 6
                      else:
                          data[x, y] = (data[currentxy[0][0], currentxy[0][1]] + data[
                              currentxy[1][0], currentxy[1][1]] + data[currentxy[2][0], currentxy[2][1]] + data[
                                            currentxy[3][0], currentxy[3][1]] + data[currentxy[4][0], currentxy[4][1]] +
                                        data[currentxy[5][0], currentxy[5][1]]) / 6

      return data