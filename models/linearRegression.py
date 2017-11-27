from math import sqrt
import pdb

def mean(values):
	return sum(values) / float(len(values))

def covariance(x, mean_x, y, mean_y):
	covar = 0.0
	for i in range(len(x)):
		covar += (x[i] - mean_x) * (y[i] - mean_y)
	return covar

def variance(values, mean):
	return sum([(x-mean)**2 for x in values])


class linearRegression:

    def coefficients(dataset):
        x = [row[0] for row in dataset]
        y = [row[1] for row in dataset]
        x_mean, y_mean = mean(x), mean(y)
        b1 = covariance(x, x_mean, y, y_mean) / variance(x, x_mean)
        b0 = y_mean - b1 * x_mean
        return [b0, b1]
    '''
    def coefficients2(x,y):
        self.coef = []
        y_mean = mean(y)
        for i in range(len(x)):
            x = [row[i] for row in x]
            x_mean = mean(x)
            x_coef = covariance(x, x_mean, y, y_mean) / variance(x, x_mean)
            y_coef = y_mean - x_coef * x_mean
            self.coef.append([x_coef,y_coef])
    '''

    def predict(self,x):
        #return self.b0 + self.b1 * instance[0]
        if isinstance(x,list) and isinstance(x[0],list):
            result = []
            for item in x:
                result.append(self.predict(item))
            return result
        else:
            sum = 0.0
            for i in range(len(x)):
                sum += self.coef[i][1] + self.coef[i][0] * x[i]
            return sum


        

    def fit(self,x,y):
        #self.b0, self.b1 = self.coefficients(x)
        self.coef = []
        self.bias = 0.0
        y_mean = mean(y)
        for i in range(len(x[0])):
            x_i = [row[i] for row in x]
            x_mean = mean(x_i)
            x_coef = covariance(x_i, x_mean, y, y_mean) / variance(x_i, x_mean)
            y_coef = y_mean - x_coef * x_mean
            self.coef.append([x_coef,y_coef])

    def __init__(self):
        pass