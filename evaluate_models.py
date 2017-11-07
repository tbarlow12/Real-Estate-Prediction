import helpers as h 
from models import neuralNet, polyReg, baselineClassifier

x, y = h.get_dataset_from_csv('sample_data.csv')

for i in range(0,len(x[0])):

    b = baselineClassifier.one_dimensional(i)

    b.fit(x,y)

    print(i,b.predict(x[0]),y[0])

