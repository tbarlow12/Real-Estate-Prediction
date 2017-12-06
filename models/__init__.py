import pdb
import numpy as np
import helpers as h
import cross_validation as cv
from copy import deepcopy

class stochastic_gd:


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

class baseline_classifier:

    def fit(self,x,y):
        self.mean = np.mean(y)
    def predict(self,x):
        if isinstance(x,list) and isinstance(x[0],list):
            result = []
            for item in x:
                result.append(self.predict(item))
            return result
        else:
            return self.mean

class lasso:
    def fit(self,x,y):
        pass
    def predict(self,x):
        pass

class ridge:
    def set_params(self,lam=.1):
        self.lam = lam
    def fit(self,x,y):
        x = np.array(x)
        y = np.array(y)
        ones = np.ones(len(x))
        x = np.column_stack((ones,x))

        xt = np.transpose(x)
        lam_ident = self.lam * np.identity(len(xt))
        inv = np.linalg.inv(np.dot(xt,x) + lam_ident)
        self.w = np.dot(np.dot(inv,xt),y)
        self.bias = self.w[0]
        self.w = self.w[1:]
        return self.w, lambda x: dot(self.w,x)

    def predict(self,x):
        if isinstance(x,list) and isinstance(x[0],list):
            result = []
            for item in x:
                result.append(self.predict(item))
            return result
        else:
            return self.bias + np.dot(self.w,x)
    
    def __init__(self,lam=.1):
        self.lam = lam

class stochastic:
    def get_gradient(self,x,y):
        y_estimate = x.dot(self.w).flatten()
        error = (y.flatten() - y_estimate)
        mse = (1.0/len(x))*np.sum(np.power(error, 2))
        gradient = -(1.0/len(x)) * error.dot(x)
        return gradient, mse

    def fit(self,x,y):
        self.w = np.array([0.0 for i in range(len(x[0]))])
        x = np.array(x)
        y = np.array(y)
        alpha = 0.5
        tolerance = 1e-5

        # Perform Stochastic Gradient Descent
        epochs = 1
        decay = 0.95
        batch_size = 10
        iterations = 0
        while True:
            order = np.random.permutation(len(x))
            train_x = x[order]
            train_y = y[order]
            b=0
            while b < len(train_x):
                tx = x[b : b+batch_size]
                ty = x[b : b+batch_size]
                gradient = self.get_gradient(tx, ty)[0]
                error = self.get_gradient(x, y)[1]
                self.w -= alpha * gradient
                iterations += 1
                b += batch_size
            
            # Keep track of our performance
            if epochs%100==0:
                new_error = get_gradient(w, train_x, train_y)[1]
                print("Epoch: %d - Error: %.4f" %(epochs, new_error))
            
                # Stopping Condition
                if abs(new_error - error) < tolerance:
                    print("Converged.")
                    break
                
            epochs += 1
            alpha = alpha * (decay ** int(epochs/1000))

    def predict(self,x):
        x = np.array(x)
        return x.dot(self.w).flatten()