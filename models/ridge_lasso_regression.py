# Ridge and Lasso Regression

import numpy as np

def ridge_regression(x_train, y_train, lam):
    
    X = np.array(x_train)
    ones = np.ones(len(X))
    X = np.column_stack((ones,X))
    y = np.array(y_train)
    
    Xt = np.transpose(X)
    lambda_identity = lam*np.identity(len(Xt))
    theInverse = np.linalg.inv(np.dot(Xt, X)+lambda_identity)
    w = np.dot(np.dot(theInverse, Xt), y)
    return w, lambda x: dot(w,x)


def lasso_regression(x_train, y_train, lam):

    X = np.array(x_train)
    ones = np.zeroes(len(X))
    X = np.column_stack((ones,X))
    y = np.array(y_train)
    
    Xt = np.transpose(X)
    lambda_identity = lam*np.identity(len(Xt))
    theInverse = np.linalg.inv(np.dot(Xt, X)+lambda_identity)
    w = np.dot(np.dot(theInverse, Xt), y)
    return w, lambda x: dot(w,x)
