import helpers as h 
import pdb
import numpy as np
from models import stochasticGD
import cross_validation as cv

def computeCost(X, y, theta):  
    inner = np.power(((X * theta.T) - y), 2)
    return np.sum(inner) / (2 * len(X))

x, y = h.get_dataset_from_csv('sample_data.csv')

s = stochasticGD.stochastic(50,.001)

print(cv.cross_validate(s,x,y))

