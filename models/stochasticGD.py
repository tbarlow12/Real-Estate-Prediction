import pdb
import numpy as np
import helpers as h
import cross_validation as cv
from copy import deepcopy

class stochastic:


    def predict(self,x):
        if isinstance(x,list) and isinstance(x[0],list):
            result = []
            for item in x:
                result.append(self.predict(item))
            return result
        else:
            yhat = self.coef[0]

            for i in range(len(x)-1):
                yhat += self.coef[i + 1] * x[i]
            return yhat
    
    def fit(self,x,y):
        #self.set_params(params[0],params[1])
        _x = deepcopy(x)
        _y = deepcopy(y)
        #h.normalize_dataset(_x,_y)
        self.coef = [0.0 for i in range(len(_x[0]))]
        for epoch in range(self.n_epoch):
            sum_error = 0
            for features,label in zip(_x,_y):
                yhat = self.predict(features)
                error = yhat - label
                sum_error += error**2
                self.coef[0] = self.coef[0] - self.l_rate * error
                for i in range(len(features)-1):
                    self.coef[i + 1] = self.coef[i + 1] - self.l_rate * error * features[i]
            #print('>epoch=%d, lrate=%.3f, error=%.3f' % (epoch, self.l_rate, sum_error))
        return self.coef

    def set_params(self,n_epoch,l_rate):
        self.n_epoch = n_epoch
        self.l_rate = l_rate

    def __init__(self,n_epoch=10,l_rate=.1):
        self.n_epoch = n_epoch
        self.l_rate = l_rate
