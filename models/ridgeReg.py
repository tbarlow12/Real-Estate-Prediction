class RidgeRegression:
    
    def predict(self,instance):
        return X.dot(self.w)

    def fit(self,x,y):
        C = X.T.dot(X) + self.lmbda*numpy.eye(X.shape[1])
        self.w = numpy.linalg.inv(C).dot(X.T.dot(y))))

    def __init__(self,lmbda=0.1):
        self.lmbda = lmbda
        