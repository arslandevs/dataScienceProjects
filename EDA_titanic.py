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
sns.heatmap(df.isna(), yticklabels=False, cmap='YlGnBu')
plt.savefig("E:\DataScience & AI\Github_repo\DataScience-projects\missing_val.png")
