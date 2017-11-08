import numpy as np
import pdb
import pandas as pd 



def gradientDescent(X, y, theta, alpha, iters):  
    temp = np.matrix(np.zeros(theta.shape))
    parameters = int(theta.ravel().shape[1])
    cost = np.zeros(iters)

    for i in range(iters):
        error = (X * theta.T) - y

        for j in range(parameters):
            term = np.multiply(error, X[:,j])
            temp[0,j] = theta[0,j] - ((alpha / len(X)) * np.sum(term))

        theta = temp
        cost[i] = computeCost(X, y, theta)

    return theta, cost

class linReg2:
    def predict(self,instance):
        pass

    def fit(self,x,y):
        year = [i[6] for i in x]
        month = [i[7] for i in x]

        m = len(year)
        x0 = np.ones(m)

        new_x = np.array([x0, year, month]).T 
        B = np.array([0,0,0])
        new_y = np.array(y)
        alpha = 0.0001

        initial_cost = cost_function(new_x, new_y, B)
        
        newB, cost_history = gradient_descent(new_x, new_y, B, alpha, 100000)

        print(newB)
        print(cost_history)

    def __init__(self):
        pass
    