import math
import pdb
import os
import numpy as np
import matplotlib 
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from random import shuffle


def k_folds(x,y,k):
    count = float(len(x))
    fold_size = math.floor(count / float(k))
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
        #print('Predicted: {}, Actual: {}'.format(predicted[i],actual[i]))
    mean_error = sum_error / float(len(actual))
    return math.sqrt(mean_error)

def get_dir(path):
    last_index = path.rfind('/')
    return path[0:last_index]

def plot_results(x_axis, actual, predictions, path):
    plt.plot(x_axis, actual, 'ro', x_axis, predictions, 'bo')
    if 'baseline' in path:
        pdb.set_trace()
    dir = get_dir(path)
    if not os.path.exists(dir):
        os.makedirs(dir)
    plt.savefig(path)
    plt.clf()

def evaluate_model(model,x,y,graph_path,include_graphs):
    results = model.predict(x)
    if graph_path is not None and include_graphs:
        x_axis = [row[0] for row in x]
        plot_results(x_axis, y, results, graph_path)
    return rmse_metric(results,y)

def cross_validate(model,x,y,name=None,include_graphs=False):
    k = 10
    x_folds, y_folds = k_folds(x,y,k)
    scores = []
    for i in range(0,k):
        x_training = (x_folds[:i] + x_folds[(i + 1):])[0]
        y_training = (y_folds[:i] + y_folds[(i + 1):])[0]
        try:
            x_test = x_folds[i]
        except IndexError:
            pdb.set_trace()
        y_test = y_folds[i]
        model.fit(x_training,y_training)
        if name is not None:
            new_name = 'graphs/{}-fold{}.png'.format(name,i)
        else:
            new_name = None
        score = evaluate_model(model,x_test,y_test,new_name,include_graphs)
        scores.append(score)
    return np.mean(scores)

    

def eval_split(model,x,y,split=.75,name=None,include_graphs=False):
    training_size = math.floor(split * len(x))
    train_x = x[0:training_size]
    train_y = y[0:training_size]
    test_x = x[training_size:]
    test_y = y[training_size:]
    model.fit(train_x,train_y)
    if name is not None:
        path = 'graphs/{}.png'.format(name)
    else:
        path = None
    score = evaluate_model(model,test_x,test_y,path,include_graphs)
    return score


def find_hypers(model,x,y,hypers):
    best_score = float('inf')
    best_params = []
    if len(hypers) == 1:

        best_params = [hypers[0][0]]
        for hyper1 in hypers[0]:
            model.set_params(hyper1)
            score = cross_validate(model,x,y)
            if score < best_score:
                best_score = score
                best_params = [hyper1]
    elif len(hypers) == 2:
        best_params = [hypers[0][0],hypers[1][0]]
        for hyper1 in hypers[0]:
            for hyper2 in hypers[1]:
                model.set_params(hyper1,hyper2)
                score = cross_validate(model,x,y)
                if score < best_score:
                    best_score = score
                    best_params = [hyper1,hyper2]
    elif len(hypers) == 3:
        best_params = [hypers[0][0],hypers[1][0],hypers[2][0]]
        for hyper1 in hypers[0]:
            for hyper2 in hypers[1]:
                for hyper3 in hypers[2]:
                    model.set_params(hyper1,hyper2,hyper3)
                    score = cross_validate(model,x,y)
                    if score < best_score:
                        best_score = score
                        best_params = [hyper1,hyper2,hyper3]
    return best_params
