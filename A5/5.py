import numpy as np
import pandas as pd
import matplotlib.pyplot as plot
import matplotlib.dates as mdate
import sklearn
import datetime
from sklearn import datasets, linear_model, metrics
# Part 1

users = pd.read_json('users.json').dropna(subset=['created','karma'], how='all')
users['created'] = users['created'].astype(int).values.reshape(-1,1)
users['karma'] = users['karma'].astype(int).values.reshape(-1,1)
X_tr, X_te, Y_tr, Y_te = sklearn.model_selection.train_test_split(users['created'].values, users['karma'].values, test_size=0.20, random_state=5)
reg = linear_model.LinearRegression()


reg.fit(X_tr.reshape(-1,1),Y_tr.reshape(-1,1))
predictor = reg.predict(X_te.reshape(-1,1))
fig, ax = plot.subplots()

plot.scatter(X_te,Y_te)
plot.xlabel('Created')
plot.ylabel('Karma')
plot.plot(X_te,predictor, color='black', linewidth=3)

coef = reg.coef_
intercept = reg.intercept_

print(coef) # A
print(intercept) # B

# The coeficient is the rate at which the response changes based on any change in the predictor
# The intercept is the mean of Y when X is 0, but there are no X values at 0 so the intercept is useless in this case
# Because the coeficient is negative it means that there is an inverse relationship->X decreases when Y increases

# Part 2

print('Test data: ' + str(metrics.mean_absolute_error(Y_te,predictor)))
print('Training data: ' + str(metrics.mean_absolute_error(Y_tr,reg.predict(X_tr.reshape(-1,1)))))

# The smaller the numbers, the better the model.
# The MAE model is not very efficient for our sampe due to the fact that there are numbers that are far away from 0


# Part 3

print('Test data: ' + str(metrics.mean_squared_error(Y_te, predictor)))
print('Training data: ' + str(metrics.mean_squared_error(Y_tr,reg.predict(X_tr.reshape(-1,1)))))

# The model fits again for smaller numbers
# Because of a few large numbers, the MAE model is even worse



# Part 4

print('Test data: ' + str(metrics.r2_score(Y_te, predictor)))
print('Training data: ' + str(metrics.r2_score(Y_tr,reg.predict(X_tr.reshape(-1,1)))))

# Thanks to the small numbers, Pearson's r is a good choice here because the numbers we get are close to 0.


# Part 5

# Based on our tests we conclude that the time when the account was created doesn't have anything to do 
# with the creation date and other factors are involved
# The best way to make the prediction more accurate is to increase the size of the sample