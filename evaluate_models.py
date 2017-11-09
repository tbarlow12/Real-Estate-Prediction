import helpers as h 
import pdb
from models import stochasticGD
import cross_validation as cv

x, y = h.get_dataset_from_csv('sample_data.csv')

s = stochasticGD.stochastic(50,.001)

print(cv.cross_validate(s,x,y))

