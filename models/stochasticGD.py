import pdb
import numpy as np
import helpers as h

class stochastic:

    def predict(self,x):
        yhat = self.coef[0]
        for i in range(len(x)-1):
            yhat += self.coef[i + 1] * x[i]
        return yhat
    
    def fit(self,x,y):
        h.normalize_dataset(x,y)
        self.coef = [0.0 for i in range(len(x[0]))]
        for epoch in range(self.n_epoch):
            sum_error = 0
            for features,label in zip(x,y):
                yhat = self.predict(features)
                error = yhat - label
                sum_error += error**2
                self.coef[0] = self.coef[0] - self.l_rate * error
                for i in range(len(features)-1):
                    self.coef[i + 1] = self.coef[i + 1] - self.l_rate * error * features[i]
            print('>epoch=%d, lrate=%.3f, error=%.3f' % (epoch, self.l_rate, sum_error))
        return self.coef

    def __init__(self,n_epoch,l_rate):
        self.n_epoch = n_epoch
        self.l_rate = l_rate
