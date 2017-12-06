import helpers as h 
import pdb
import models
import cross_validation as cv
from sklearn.linear_model import Ridge, Lasso, LinearRegression, SGDClassifier
import numpy as np


zip_code_separated_data = h.get_feature_vector_separate(
    'data_collection/Sample Data/final_feature_set.csv',
    ['MonthId','Crime Code'],
    'Zip_MedianValuePerSqft_AllHomes')

zip_codes = []
sk_linear = []
sk_ridge = [] 
sk_lasso = []
sk_sgd = []
baseline = []

for zip_code in zip_code_separated_data:
    features = zip_code_separated_data[zip_code][0]
    labels = zip_code_separated_data[zip_code][1]
    
    zip_codes.append(zip_code)

    linear_score = cv.cross_validate(LinearRegression(),features,labels)
    ridge_score = cv.cross_validate(Ridge(),features,labels)
    lasso_score = cv.cross_validate(Lasso(),features,labels)
    sgd_score = cv.cross_validate(SGDClassifier(),features,labels)

    sk_linear.append(linear_score)
    sk_ridge.append(ridge_score)
    sk_lasso.append(lasso_score)
    sk_sgd.append(sgd_score)

    baseline_score = cv.cross_validate(models.baseline(),features,labels)
    baseline.append(baseline_score)


print('Sklearn Linear: ', np.mean(sk_linear),np.std(sk_linear))
print('Sklearn Ridge: ', np.mean(sk_ridge),np.std(sk_ridge))
print('Sklearn Lasso: ', np.mean(sk_lasso),np.std(sk_lasso))
print('Sklearn SGD: ', np.mean(sk_sgd),np.std(sk_sgd))
print('Baseline: ', np.mean(baseline),np.std(baseline))

