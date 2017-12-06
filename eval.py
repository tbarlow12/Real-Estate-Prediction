import helpers as h 
import pdb
from models import stochasticGD, linearRegression 
import cross_validation as cv
from sklearn.linear_model import Ridge, Lasso, LinearRegression
import numpy as np


zip_code_separated_data = h.get_feature_vector_separate(
    'data_collection/Sample Data/final_feature_set.csv',
    ['MonthId','Crime Code'],
    'Zip_MedianValuePerSqft_AllHomes')

zip_codes = []
sk_linear = []
sk_ridge = [] 
sk_lasso = []
for zip_code in zip_code_separated_data:
    features = zip_code_separated_data[zip_code][0]
    labels = zip_code_separated_data[zip_code][1]

    linear_score = cv.cross_validate(LinearRegression(),features,labels)
    ridge_score = cv.cross_validate(Ridge(),features,labels)
    lasso_score = cv.cross_validate(Lasso(),features,labels)

    zip_codes.append(zip_code)

    sk_linear.append(linear_score)
    sk_ridge.append(ridge_score)
    sk_lasso.append(lasso_score)

    hypers = cv.find_hypers(stochasticGD.stochastic(),features,labels,[[50,40,30,20,10,5],[1,.1,.01,.001,.0001,.00001]])

print(np.mean(sk_linear),np.std(sk_linear))
print(np.mean(sk_ridge),np.std(sk_ridge))
print(np.mean(sk_lasso),np.mean(sk_lasso))

''' s = stochasticGD.stochastic()
    hypers = cv.find_hypers(s,features,labels,[[50,40,30,20,10,5],[1,.1,.01,.001,.0001,.00001]])
    
    print(hypers)
    s.set_params(hypers[0],hypers[1])
    print(cv.cross_validate(s,features,labels))'''


'''
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



