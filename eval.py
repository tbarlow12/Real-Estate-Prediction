import helpers as h 
import pdb
from models import baseline_classifier, ridge 
import cross_validation as cv
from sklearn.linear_model import Ridge, Lasso, LinearRegression, SGDClassifier
import numpy as np
from copy import deepcopy

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


def get_all_features_except(exclude_list):
    with open('all_features.txt') as f:
        lines = f.readlines()
        result = []
        for line in lines:
            in_exclude = False
            for exclude in exclude_list:
                if line.startswith(exclude):
                    in_exclude = True
            if not in_exclude:
                result.append(line.strip())
        return result

def evaluate_model(model,features):
    zip_code_separated_data = h.get_feature_vector_separate(
        'data_collection/Sample Data/final_feature_set.csv',
        features, #features
        'Zip_MedianValuePerSqft_AllHomes') #label
    scores = []
    for zip_code in zip_code_separated_data:
        x = zip_code_separated_data[zip_code][0]
        y = zip_code_separated_data[zip_code][1]
        if len(x) >= 10:
            scores.append(cv.cross_validate(model,x,y))
    if len(scores) == 0:
        return None
    return np.mean(scores)

def find_best_features(model):
    all_features = get_all_features_except(['Crime','Victim','Zip Code','MonthId','Zip_MedianValuePerSqft_AllHomes','Zip_Zhvi'])
    best_features = ['MonthId']
    max_features = 1000
    best_overall_score = float('inf')
    has_improved = True
    while has_improved:
        has_improved = False
        best_feature = None
        best_feature_score = float('inf')
        for feature in all_features:
            if feature not in best_features:
                temp_features = deepcopy(best_features)
                temp_features.append(feature)
                score = evaluate_model(model,temp_features)
                if score is not None and score < best_feature_score:
                    best_feature = feature
                    best_feature_score = score
        if best_feature_score < best_overall_score:
            has_improved = True
            best_features.append(best_feature)
            best_overall_score = best_feature_score
            print(best_features)
    return best_features, best_overall_score
            
    


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
    #evaluate_separated()
    ridge_features, ridge_score = find_best_features(Ridge())

    '''
    Results for SKRidge
    SKRidge ['MonthId', 'Zip_MedianRentalPrice_DuplexTriplex', 'Zip_MedianRentalPricePerSqft_CondoCoop', 'Zip_Listings_PriceCut_SeasAdj_AllHomes', 'Zip_ZriPerSqft_AllHomes'] 5.51085665045
    '''
    print('SKRidge',ridge_features,ridge_score)
    

    #linear_features, linear_score = find_best_features(LinearRegression())
    #print('SKLinear',linear_features,linear_score)

    lasso_features, lasso_score = find_best_features(Lasso())
    print('SKLasso',lasso_features,lasso_score)

    sgd_features, sgd_score = find_best_features(SGDClassifier())
    print('SGDClassifier',sgd_features,sgd_score)

if __name__ == '__main__':
    main()