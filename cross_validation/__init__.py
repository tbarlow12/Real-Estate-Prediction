import math
import pdb
import numpy as np

def k_folds(x,y,k):
    count = float(len(x))
    fold_size = math.ceil(count / float(k))
    x_folds = []
    y_folds = []
    start_index = 0
    while(start_index < count):
        if start_index < (count - fold_size):
            x_folds.append(x[start_index:start_index + fold_size])
            y_folds.append(y[start_index:start_index + fold_size])
        else:
            x_folds.append(x[start_index:])
            y_folds.append(y[start_index:])
        start_index += fold_size
    return x_folds, y_folds

def rmse_metric(predicted, actual):
    sum_error = 0.0
    for i in range(len(actual)):
        prediction_error = predicted[i] - actual[i]
        sum_error += (prediction_error ** 2)
    mean_error = sum_error / float(len(actual))
    return math.sqrt(mean_error)

def evaluate_model(model,x,y):
    results = model.predict_batch(x)
    return rmse_metric(results,y)
    

def cross_validate(model,x,y):
    k = 2
    x_folds, y_folds = k_folds(x,y,k)
    scores = []
    for i in range(0,k):
        x_training = (x_folds[:i] + x_folds[(i + 1):])[0]
        y_training = (y_folds[:i] + y_folds[(i + 1):])[0]
        x_test = x_folds[i]
        y_test = y_folds[i]
        model.fit(x_training,y_training)
        scores.append(evaluate_model(model,x_test,y_test))
    return np.mean(scores)
