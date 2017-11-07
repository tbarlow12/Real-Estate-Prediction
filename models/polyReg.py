import numpy as np
import pdb 
import math



class polyReg:

    def predict(self,instance):
        pass

    def fit(self,x,y):
        features = np.array(x)
        labels = np.array(y).T
        pdb.set_trace()

    def __init__(self,degree):
        self.degree = degree        
