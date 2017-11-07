import math
import pdb

class one_dimensional:
    def predict(self,x):
        return x[self.dim] * self.weights[0] + self.weights[1]

    def fit(self,x,y):
        # Basic computations to save a little time.
        x = [i[self.dim] for i in x]
        length = len(x)
        sum_x = sum(x)
        sum_y = sum(y)

        # Σx^2, and Σxy respectively.
        sum_x_squared = sum(map(lambda a: a * a, x))
        sum_of_products = sum([x[i] * y[i] for i in range(length)])

        # Magic formulae!
        a = (sum_of_products - (sum_x * sum_y) / length) / (sum_x_squared - ((sum_x ** 2) / length))
        b = (sum_y - a * sum_x) / length
        self.weights = [a, b]

    def __init__(self,dim):
        self.dim = dim