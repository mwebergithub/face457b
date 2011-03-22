#!/usr/bin/env python
##################################################
# Example for Kohonen Map
#
# Clusters random 2D coordinates in range [0,1]
# with a Kohonen Map of 5x5 neurons.
#
# Note: you need pylab to show the results
##################################################

__author__ = 'Thomas Rueckstiess, ruecksti@in.tum.de'

import pylab
from scipy import random
from custom_kohonen import KohonenMap
#from pybrain.structure.modules import KohonenMap

from pylab import ion, ioff, figure, draw, contourf, clf, show, hold, plot
from scipy import diag, arange, meshgrid, where
from numpy.random import multivariate_normal

from numpy import zeros

cluster_data = []
#means = [(-1,0),(2,4),(3,1)]
means = [(-10,10),(10,10),(0,0),(10,-10)]
cov = [diag([1,1]), diag([0.5,1.2]), diag([1.5,0.7]), diag([1.5,0.7])]
for n in xrange(400):
  for klass in range(len(means)):
    cluster_data.append(multivariate_normal(means[klass],cov[klass]))

som = KohonenMap(2, 9, 9)

pylab.ion()
p = pylab.plot(som.neurons[:,:,0].flatten(), som.neurons[:,:,1].flatten(), 's')
pylab.axis([-15,15,-15,15])

i = 0
for j in range(20):
  print j
  for data in cluster_data:
      i += 1
      # one forward and one backward (training) pass
      som.activate(data)
      som.backward()

      # plot every 100th step
      if i % 100 == 0:
          p[0].set_data(som.neurons[:,:,0].flatten(), som.neurons[:,:,1].flatten())
          pylab.draw()
