# Working models:
- Stochastic gradient descent

# Things to do:
- Combine data files for more informative datasets
    - E.g. Combine 1 bedroom, 2 bedroom, 3 bedroom, etc. files into one file with the number of bedrooms as a feature
- Stochastic gradient descent
    - Run cross validation with different hyper params (learning rate and epochs) to see which gives us the best results 
- Actually encode categorical data
    - Currently being treated as continuous data... Need to apply "one hot encoding", having dummy features for each possible value
    - Going to create MASSIVE files (horizontally at least)
    - DON'T do this... Go for feature hashing
- Improve model evaluation
    - Compute R-squared value
    - Plot points
- How to decide which feature are most important?
- Choose one variable and use the others as features
    - PCA or SVD to determine features
- Add other economic measures
    - Daily closings of dow
    - GDP
    - During recession??
- Maybe not predict specific price, but *predict specific rank*

# Progress
- 11/8/17
    - Stochastic gradient descent implemented
    - RMSE metric for evaluation implmented
    - K fold cross validation implemented
    - Non-normalized RMSE of 2806.345 with SGD on sample data... Not sure if that's good or bad, but we got something working and evaluated

# Plans
- Pass ML
- Graduate
- Start sweet company# cs-6490-final
