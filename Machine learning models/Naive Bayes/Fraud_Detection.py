"""Here we'll explore the dataset for the credit card faraud detection using naive bayes.
And predict what will the fraudelent transactions!"""

# importing necessary libraries
from sklearn.metrics import confusion_matrix, precision_score, f1_score
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Loading data
df = pd.read_csv("E:\DataScience & AI\Github_repo\creditcard.csv\creditcard.csv")
df.shape
df.describe()
df.info

val_count = df.Class.value_counts()  # gives the number of 1's and 0's in the the class column
# visualizing class column
# Class column specifies that the traction belong to which class
# 1 = Fraudelent transaction; 0 = Non-fradulaent  transaction
print("Class column:")
fig, ax = plt.subplots(1, 1)
# here "%1.1f%%" says represents width of 1 and precision of 1 in the output
ax.pie(val_count, explode=[0, 0.1], autopct='%1.1f%%',
       labels=['Not fraud', 'Fraud'], colors=['orange', 'blue'])
plt.axis('equal')
# print(plt.pie.__doc__)
# ----------------

# Splitting data in train and test using sklearn train_test_split

y = df["Class"].values
X = df.drop(['Class'], axis=1).values
X.shape
y.shape
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = GaussianNB()

X_train.shape
y_train.shape

# #list2:0 we know that the in this ml model there is no storing of the weighths and
# optimization techniques, it only predict the expected probablities that's why it is a fast model.
model.fit(X_train, y_train)  # training of naive bayes

# Model predictions
y_pred = model.predict(X_test)
y_pred
# here are the probablities of the individual credict card
y_pred_prob = model.predict_proba(X_test)
y_pred_prob
y_train_pred = model.predict(X_train)

# Confusion matrix is a handy tool to check how much are the true predictions.
confusion_mat = confusion_matrix(y_train, y_train_pred)  # both parameter of it are labels
confusion_mat

# from the heatmap it can be shown easily that very small number of trasanctionsa
# are Fraudelent major are non-Fraudelent
sns.heatmap(confusion_mat, square=True, annot=True, fmt='d',)

# Calculating precison and f1 scares on the predctions
f1_score(y_test, y_pred)
precision_score(y_test, y_pred)

f1_score(y_train, y_train_pred)
precision_score(y_train, y_train_pred)
