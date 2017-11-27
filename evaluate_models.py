import helpers as h 
import pdb
from models import stochasticGD, linearRegression 
import cross_validation as cv
from sklearn import linear_model
import numpy as np

#x, y = h.load_encoded('City_MedianListingPrice_1Bedroom.csv')

features, labels = h.featurize_file('Sample Data/california/90001-CA.csv')


clf = linear_model.LinearRegression()
s = stochasticGD.stochastic()
hypers = cv.find_hypers(s,features,labels,[[50,40,30,20,10,5],[1,.1,.01,.001,.0001,.00001]])
print(hypers)
s.set_params(hypers[0],hypers[1])

myLG = linearRegression.linearRegression()

print(cv.cross_validate(myLG,features,labels))
print(cv.cross_validate(s,features,labels))
print(cv.cross_validate(clf,features,labels))


'''

s = stochasticGD.stochastic(50,.001)
#print(cv.cross_validate(s,features,labels))

x =[
    [1,2],
    [2,3],
    [4,5],
    [6,7]
]
y = [3,5,9,13]

print(cv.cross_validate(s,x,y))

clf = linear_model.LinearRegression()

clf.fit(x,y)
print(cv.cross_validate(s,x,y))
print(cv.cross_validate(clf,x,y))
'''

