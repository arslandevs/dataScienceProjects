# Naive Bayes

![Alt Text](https://github.com/SyedArsalanAmin/Machine-Learning-Models/blob/master/nb_gif.gif)




Naive bayes is a machine learning algorithm based on bayes theorum. Which is primarily a
theorum based on __probablities__.

__Assumption__ : There should be no covariance between the variables or the dimensions._

_Download dataset(creditcardfraud) :_ https://www.kaggle.com/mlg-ulb/creditcardfraud/download

_Load dataset(text classifier)_ : from sklearn.datasets import fetch_20newsgroups
# Advantages
- Naive bayes models are _Fast_. It converges faster to the global minimum.
- Simple algorithms.
- Suitable for high dimensional data. Because for instance two points on average are more seperated on higher dimensions than in lower dimensions. That's why Naive Bayes works well as the dimentionality of the data increases.
- Easily interpretable.
- It has few tunable parameter as compared to the other algorithms.
- Performs well on categorical data.
- For very well seperated data it performs fantastic.
- It handles missing values.
- It don't requires feature scaling.
- Also it don't require feature scaling as most of the algorithms require.
- It is _Robust_ to outliers.
# Disadvantages
- Major disadvantage of Naive Bayes is that we know in real life data it is almost impossible that we get data that is totally independent and have zero covariance. That's why as the features of the data increases the probability that they relate to each other also increases and this ultimately affects the model performance.
- If for categorical data any sample which is not seen in the training and encountered in the test data then model will assign zero probability for it.
# Applications
- It is used for sentiment analysis.
- It is used for spam classification.
- It is used for twitter sentiment analysis.
- Also for document categorization.

_If you want some model that works well and make predictions fast then it is a good choice._
