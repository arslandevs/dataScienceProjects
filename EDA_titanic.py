import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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
