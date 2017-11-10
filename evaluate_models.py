import helpers as h 
import pdb
from models import stochasticGD
import cross_validation as cv
from sklearn import linear_model
import numpy as np

x, y = h.load_encoded('City_MedianListingPrice_1Bedroom.csv')

s = stochasticGD.stochastic(50,.001)
clf = linear_model.LinearRegression()
clf.fit(x,y)
print(cv.cross_validate(s,x,y))
print(cv.cross_validate(clf,x,y))

