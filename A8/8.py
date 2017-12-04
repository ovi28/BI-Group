import numpy as np
import pandas as pd
import sklearn
import scipy.stats as stats
from sklearn import linear_model, metrics
from sklearn.model_selection import KFold, cross_val_predict

#part 1.1
# Accuracy is how close the guesses are to being right. High accuracy is when the guesses are close to being right
# Precission refers to the guesses being closely clustered to each other

#part 1.2
# The difference between precision and recall is item relevancy when faced with selecting instances from a larger set.
# Recall measures how many relevant instances are selected when compared to all the instances which are available and precision refers to how many of the selected instances are relevant.

#part 2.1
# T-tests are a test type that can help us see wheter or not we can infer anything supported by a hypothesis from our data
# We can get P-values which give us a percentile probability of the hypothesis being true

brain_df = pd.read_csv('brain_size.csv', delimiter=';', index_col=0)
brain_df = brain_df[brain_df['Height'] != '.']
height_data = brain_df['Height'].values.astype(float)
height_data.shape

t, P = stats.ttest_1samp(height_data,71)

print("T-value: " + str(t))
print("P-value: " + str(P))
# The sample is at -3.8 deviation from the mean and the probability of confirming a null hypothesis is 0.04%
# In conclusion, our sample does not match the mean height of the population

t, P = stats.ttest_1samp(height_data,68.4)

print("T-value: " + str(t))
print("P-value: " + str(P))
# In this case, the mean value and the probability are showing us that the sample matches the population
