import helpers as h 
import pdb
from models import stochasticGD, linearRegression 
import cross_validation as cv
import numpy as np

data = h.get_feature_vector_separate(
    'Sample Data/final_feature_set.csv',
    ['MonthId'],
    'Zip_MedianValuePerSqft_AllHomes')
pdb.set_trace()
