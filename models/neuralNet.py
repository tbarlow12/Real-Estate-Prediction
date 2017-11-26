import numpy as np
import pdb

def nonlin(x,deriv=False):
    if(deriv==True):
        return x*(1-x)
    return 1/(1+np.exp(-x))

class neuralNet:
    
    def predict(self,x):
        pass

    def fit(self,x,y):
        pass

    def __init__(self):
        pass


# http://neuralnetworksanddeeplearning.com/chap2.html, an long chapter on backpropagation and code that implements a neural network without libraries.