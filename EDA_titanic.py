from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pyforest
%matplotlib inline

df = pd.read_csv("E:\\DataScience & AI\\Github_repo\\DataScience-projects\\titanic_train.csv")
df.head()

df['Survived'].value_counts()

df.info()

df.describe()

df.isna()


df[df['Age'].isna()]

df.dtypes

df.isnull()

# to see the missing values in a proper way use seaborn
# here you can see the cabin and age has missing values but cabin has more.
sns.set_style("whitegrid")
sns.heatmap(df.isna(), yticklabels=False, cmap='YlGnBu')
plt.savefig("E:\DataScience & AI\Github_repo\DataScience-projects\missing_val.png")

sns.countplot('Survived', data=df, hue='Sex')

sns.countplot('Pclass', data=df, hue='Sex', palette='rainbow')

sns.jointplot('Age', 'Survived', data=df, kind='hex')

sns.jointplot('Age', 'Survived', data=df, kind='reg')


sns.distplot(df['Age'].dropna(), kde=False, bins=50, color='black')

sns.countplot('SibSp', data=df)


sns.jointplot('Fare', 'Age', data=df, kind='reg')

sns.jointplot('Fare', 'Age', data=df, kind='hex')


sns.boxplot('Pclass', 'Age', data=df)
df.head(2)

# df['Pclass'].values

df[['Age', 'Pclass']]


def impute_age(cols):

    age = cols[0]
    pclass = cols[1]

    if pd.isnull(age):
        if pclass == 0:
            return 37
        elif pclass == 1:
            return 29
        else:
            return 24
    else:
        return age


df['Age'] = df[['Age', 'Pclass']].apply(impute_age, axis=1)

sns.heatmap(df.isnull())  # now no missing age values


pd.get_dummies(df['Embarked'], drop_first=True).head()

embark = pd.get_dummies(df['Embarked'], drop_first=True).head()
sex = pd.get_dummies(df['Sex'], drop_first=True).head()

df.drop(['Sex', 'Cabin', 'Embarked', 'Name', 'Ticket'], axis=1, inplace=True)
df.head()

df = pd.concat([df, embark, sex], axis=1)

df.head()

# Survived is dependent feature remaining are independent

df.drop('Survived', axis=1).head()

df['Survived'].head()

X_train, X_test, y_train, y_test = train_test_split(
    df.drop('Survived', axis=1), df['Survived'], random_state=100, test_size=0.30)

X_train.head()
y_train.head()

model = LogisticRegression()
model.fit(X_train, y_train)

predictions = model.predict(X_test)

accuracy = confusion_matrix(y_test, predictions)


accuracy = accuracy_score(y_test, predictions)

accuracy

predictions


print(classification_report(y_test, predictions))
