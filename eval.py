import helpers as h 
import pdb
from models import baseline_classifier, ridge 
import cross_validation as cv
from sklearn.linear_model import Ridge, Lasso, LinearRegression, SGDClassifier
import numpy as np

def evaluate_separated():


    zip_code_separated_data = h.get_feature_vector_separate(
        'data_collection/Sample Data/final_feature_set.csv',
        ['MonthId','total'], #features
        'Zip_MedianValuePerSqft_AllHomes') #label

    zip_codes = []
    sk_linear = []
    sk_ridge = [] 
    sk_lasso = []
    sk_sgd = []

    baseline = []
    my_ridge = []

    for zip_code in zip_code_separated_data:
        features = zip_code_separated_data[zip_code][0]
        labels = zip_code_separated_data[zip_code][1]
        
        zip_codes.append(zip_code)

        linear_score = cv.cross_validate(LinearRegression(),features,labels,'Linear')
        ridge_score = cv.cross_validate(Ridge(),features,labels)
        lasso_score = cv.cross_validate(Lasso(),features,labels)
        sgd_score = cv.cross_validate(SGDClassifier(),features,labels)

        sk_linear.append(linear_score)
        sk_ridge.append(ridge_score)
        sk_lasso.append(lasso_score)
        sk_sgd.append(sgd_score)

        baseline_score = cv.cross_validate(baseline_classifier(),features,labels)
        baseline.append(baseline_score)
        

        ridge_hypers = cv.find_hypers(ridge(),features,labels,[[10,1,.1,.01,.001,.0001]])
        ridge_model = ridge(ridge_hypers[0])
        my_ridge_score = cv.cross_validate(ridge_model,features,labels)
        my_ridge.append(my_ridge_score)



    print('Sklearn Linear: ', np.mean(sk_linear),np.std(sk_linear))
    print('Sklearn Ridge: ', np.mean(sk_ridge),np.std(sk_ridge))
    print('Sklearn Lasso: ', np.mean(sk_lasso),np.std(sk_lasso))
    print('Sklearn SGD: ', np.mean(sk_sgd),np.std(sk_sgd))
    print('Baseline: ', np.mean(baseline),np.std(baseline))
    print('My Ridge: ', np.mean(my_ridge),np.std(my_ridge))

def evaluate_together():
    zip_code_data = h.get_feature_vector_together(
        'data_collection/Sample Data/final_feature_set.csv',
        ['MonthId','total'], #features
        'Zip_MedianValuePerSqft_AllHomes') #label
    
    features = zip_code_data[0]
    labels = zip_code_data[1]

    linear_score = cv.cross_validate(LinearRegression(),features,labels)
    ridge_score = cv.cross_validate(Ridge(),features,labels)
    lasso_score = cv.cross_validate(Lasso(),features,labels)
    #sgd_score = cv.cross_validate(SGDClassifier(),features,labels)

    baseline_score = cv.cross_validate(baseline_classifier(),features,labels)

    print('Sklearn Linear: ', linear_score)
    print('Sklearn Ridge: ', ridge_score)
    print('Sklearn Lasso: ', lasso_score)
    #print('Sklearn SGD: ', sgd_score)
    print('Baseline: ', baseline_score)


def main():
    #evaluate_together()
    evaluate_separated()

if __name__ == '__main__':
    main()