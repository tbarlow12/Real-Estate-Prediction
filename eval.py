import helpers as h 
import pdb
from models import baseline_classifier, ridge 
import cross_validation as cv
from sklearn.linear_model import Ridge, Lasso, LinearRegression, SGDClassifier
import numpy as np

def print_stats(model_name,cv_list,split_list):
    while len(model_name) < 8:
        model_name += ' '
    print('{0}\t{1:.3f}\t{2:.3f}\t{3:.3f}\t{4:.3f}'.format(
        model_name,
        np.mean(cv_list),
        np.std(cv_list),
        np.mean(split_list),
        np.std(split_list)
    ))

def evaluate_separated():


    zip_code_separated_data = h.get_feature_vector_separate(
        'data_collection/Sample Data/final_feature_set.csv',
        ['MonthId','total','Crime Code'], #features
        'Zip_MedianValuePerSqft_AllHomes') #label

    zip_codes = []

    sk_linear_cv = []
    sk_linear_split = []
    
    sk_ridge_cv = []
    sk_ridge_split = []

    sk_lasso_cv = []
    sk_lasso_split = []

    sk_sgd_cv = []
    sk_sgd_split = []

    baseline_cv = []
    baseline_split = []

    my_ridge_cv = []
    my_ridge_split = []

    for zip_code in zip_code_separated_data:
        x = zip_code_separated_data[zip_code][0]
        y = zip_code_separated_data[zip_code][1]
        
        zip_codes.append(zip_code)


        sk_linear_cv.append(cv.cross_validate(LinearRegression(),x,y))
        sk_linear_split.append(cv.eval_split(LinearRegression(),x,y,name='{}/sk_linear'.format(zip_code)))

        sk_ridge_cv.append(cv.cross_validate(Ridge(),x,y))
        sk_ridge_split.append(cv.eval_split(Ridge(),x,y,name='{}/sk_ridge'.format(zip_code)))

        sk_lasso_cv.append(cv.cross_validate(Lasso(),x,y))
        sk_lasso_split.append(cv.eval_split(Lasso(),x,y,name='{}/sk_lasso'.format(zip_code)))

        sk_sgd_cv.append(cv.cross_validate(SGDClassifier(),x,y))
        sk_sgd_split.append(cv.eval_split(SGDClassifier(),x,y,name='{}/sk_sgd'.format(zip_code)))

        baseline_cv.append(cv.cross_validate(baseline_classifier(),x,y))
        baseline_split.append(cv.eval_split(baseline_classifier(),x,y,name='{}/baseline'.format(zip_code)))

        my_ridge_cv.append(cv.cross_validate(ridge(),x,y))
        my_ridge_split.append(cv.eval_split(ridge(),x,y,name='{}/my_ridge'.format(zip_code)))
        

    print('Model   \tCV Mean\tCV Std\tSplit Mean\tSplit Std')
    print_stats('SkLinear',sk_linear_cv,sk_linear_split)
    print_stats('SkRidge',sk_ridge_cv,sk_ridge_split)
    print_stats('SkLasso',sk_lasso_cv,sk_lasso_split)
    print_stats('SkSGD',sk_sgd_cv,sk_sgd_split)
    print_stats('Baseline',baseline_cv,baseline_split)
    print_stats('My Ridge',my_ridge_cv,my_ridge_split)


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