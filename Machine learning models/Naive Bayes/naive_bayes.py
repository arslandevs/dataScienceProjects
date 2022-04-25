"""Here we'll implement simple guassian naive bayes algorithm using sklearn.
Gausian Naive bayes works on probablities and we assume that there is
no covariance in between the dimensions or the features."""

# Importing necessary libraries
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.naive_bayes import GaussianNB
sns.set()

# Generating data
X, y = make_blobs(100, 2, centers=2)
np.shape(X)
np.shape(y)
plt.scatter(X[:, 0], X[:, 1])

# model building
model = GaussianNB()
model.fit(X, y)  # X fearures are trained with y labels

# Model Prediction

# predicting on single value
y1 = np.array([9.08, -2.21])
model.predict([y1])

# predicting on array of values
y2 = np.random.randint(-10, 10, (100, 2))
# give the same shape of the data here as provided in the train dataset i.e 2D
model.predict(y2)
plt.scatter(X[:, 0], X[:, 1], c=y, s=50, cmap='RdBu')
lim = plt.axis()
plt.scatter(y2[:, 0], y2[:, 1], c=y, s=50, cmap='RdBu')

model.predict_proba([[0.1, 0.3]])
