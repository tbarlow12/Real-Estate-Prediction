import helpers as h 
import pdb
from models import baseline_classifier, ridge, lasso, linear
import cross_validation as cv
from sklearn.linear_model import Ridge, Lasso, LinearRegression, SGDClassifier
import numpy as np
from copy import deepcopy
import operator

def print_stats(model_name,cv_list,test_scores,train_scores,zip_codes):
    print('Best Zip Codes')
    while len(model_name) < 8:
        model_name += ' '
    sorted(zip_codes,key=operator.itemgetter(1))
    sorted(zip_codes,key=operator.itemgetter(2),reverse=True)
    for z in zip_codes[0:5]:
        print(z)
    print('Model   \tCV Mean\tCV Std\tTest Mean\tTest Std\tTrain Mean\tTrain Std')
    print('{0}\t{1:.3f}\t{2:.3f}\t{3:.3f}\t{4:.3f}\t{5:.3f}\t{6:.3f}'.format(
        model_name,
        np.mean(cv_list),
        np.std(cv_list),
        np.mean(test_scores),
        np.std(test_scores),
        np.mean(train_scores),
        np.std(train_scores)
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


def evaluate_separated(model,features,name):

    zip_code_separated_data = h.get_feature_vector_separate(
        'data_collection/Sample Data/final_feature_set.csv',
        features, #features
        'Zip_MedianValuePerSqft_AllHomes') #label

    zip_codes = []

    cv_scores = []
    test_scores = []
    train_scores = []

    for zip_code in zip_code_separated_data:
        x = zip_code_separated_data[zip_code][0]
        y = zip_code_separated_data[zip_code][1]
        

        cv_scores.append(cv.cross_validate(model,x,y))
        test_score, train_score = cv.eval_split(model,x,y,name='{}/{}'.format(zip_code,name),include_graphs=True)
        test_scores.append(test_score) 
        train_scores.append(train_score)  
        zip_codes.append([zip_code,test_score,len(x)])     

    print_stats(name,cv_scores,test_scores,train_scores,zip_codes)

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

def find_hypers_multiple(model,features,hypers):
    zip_code_separated_data = h.get_feature_vector_separate(
        'data_collection/Sample Data/final_feature_set.csv',
        features, #features
        'Zip_MedianValuePerSqft_AllHomes') #label
    votes = {}
    for zip_code in zip_code_separated_data:
        x = zip_code_separated_data[zip_code][0]
        y = zip_code_separated_data[zip_code][1]
        best_hypers = cv.find_hypers(model,x,y,hypers)
        if best_hypers[0] in votes:
            votes[best_hypers[0]] += 1
        else:
            votes[best_hypers[0]] = 1
    sorted_votes = sorted(votes.items(), key=operator.itemgetter(1))
    pdb.set_trace()

def evaluate_model(model,features):
    zip_code_separated_data = h.get_feature_vector_separate(
        'data_collection/Sample Data/final_feature_set.csv',
        features, #features
        'Zip_MedianValuePerSqft_AllHomes') #label
    scores = []
    if len(zip_code_separated_data) < 10:
        return None
    for zip_code in zip_code_separated_data:
        x = zip_code_separated_data[zip_code][0]
        y = zip_code_separated_data[zip_code][1]
        if len(x) >= 20:
            scores.append(cv.cross_validate(model,x,y))
    if len(scores) == 0:
        return None
    return np.mean(scores)

def find_best_features(model):
    all_features = get_all_features_except(['Crime','Victim','Zip Code','MonthId','Zip_MedianValuePerSqft_AllHomes','Zip_Zhvi'])
    best_features = ['MonthId']
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
                    print(best_feature, best_feature_score)
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
    '''
    Results for SKRidge
    SKRidge ['MonthId', 'Zip_MedianRentalPrice_DuplexTriplex', 'Zip_MedianRentalPricePerSqft_CondoCoop', 'Zip_Listings_PriceCut_SeasAdj_AllHomes', 'Zip_ZriPerSqft_AllHomes'] 5.51085665045

    Results for My Ridge
    My Ridge ['MonthId', 'Zip_MedianListingPricePerSqft_4Bedroom', 'Zip_MedianListingPrice_3Bedroom', 'Zip_PriceToRentRatio_AllHomes', 'Zip_ZriPerSqft_AllHomes'] 13.1522008048
    
    Results for My Linear
    My Linear ['MonthId', 'Zip_MedianListingPricePerSqft_4Bedroom', 'Zip_MedianListingPrice_3Bedroom'] 14.5526363015
    
    linear_features, linear_score = find_best_features(linear())
    print('My Linear', linear_features, linear_score)
    
    ridge_features, ridge_score = find_best_features(ridge())
    print('My Ridge',ridge_features,ridge_score)
    '''
    ridge_features = ['MonthId', 'Zip_MedianListingPricePerSqft_4Bedroom', 'Zip_MedianListingPrice_3Bedroom', 'Zip_PriceToRentRatio_AllHomes', 'Zip_ZriPerSqft_AllHomes']
    linear_features = ['MonthId', 'Zip_MedianListingPricePerSqft_4Bedroom', 'Zip_MedianListingPrice_3Bedroom']
    
    evaluate_separated(ridge(),ridge_features,'Ridge')
    evaluate_separated(linear(),linear_features,'Linear')


    '''
    lasso_features, lasso_score = find_best_features(lasso())
    print('My Lasso', lasso_features,lasso_score)
    '''

    #hyper = find_hypers_multiple(ridge(),['MonthId', 'Zip_MedianRentalPricePerSqft_Studio'],[[10,1,.1,.01,.001,.0001]])
    #print(hyper)
    
    '''
    sklinear_features, sklinear_score = find_best_features(LinearRegression())
    print('SKLinear',sklinear_features,sklinear_score)
    
    sklasso_features, sklasso_score = find_best_features(Lasso())
    print('SKLasso',sklasso_features,sklasso_score)

    sksgd_features, sksgd_score = find_best_features(SGDClassifier())
    print('SGDClassifier',sksgd_features,sksgd_score)
    '''

if __name__ == '__main__':
    main()