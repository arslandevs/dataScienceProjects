# **Deep Neural Network Training**

>## **Contents**:
1. Metrics
2. Accuracy and Loss
3. Visualizing missing values
4. Correlations
5. Target_feature (encoded_specimen)
6. DagsHub Charts
7. Models Comparison
8. Links 

I used Tensorflow to implement deep neural network for binary-classification problem. For I took temp_0-8, humid_0-8, gas_scan_0-8 and gas_scan_cnt. With the target "encoded_specimen."
## **1. Metrics**:
```
Accuracy : 0.9917
Val_acc : 0.9917
Loss : 0.0381
Val_loss : 0.0380
```
## **2. Accuracy and Loss**
The accuracy and loss for both training and test data are follows.

![alt text](https://github.com/OmdenaAI/Dryad/blob/task-3-gas-classification/DNN_Syed_Arsalan_Amin/acc_loss.png)
- There are no **missing values** in the taken data. But there are **nan** entries in the dataset.
- Trained on 1000 epochs with batch_size of 64 with neurons of 128 and 32 in layer 1 and layer 2.
- Tuned hyperparameters for optimal performance.

## **3. Visualizing missing values**
In the figure below you can see after drpping above mentioned columns all the remaining data doesn't have missing values.

![alt text](https://github.com/OmdenaAI/Dryad/blob/task-3-gas-classification/DNN_Syed_Arsalan_Amin/missing_values.png)
## **4. Correlations**
In the correlation plot you can see which entries are more related to each other and yes the entries whose correlation have tendency toward higher in the right bar **(close to 1)** are more related to each other and instead of taking all that entries you can take any one them.

![alt text](https://github.com/OmdenaAI/Dryad/blob/task-3-gas-classification/DNN_Syed_Arsalan_Amin/corr_plot.png)
## **5. Target_feature (encoded_specimen)**
This is the target feature on which we are training our binary classification model. This include **im_smoke** and **clean_air**.

![alt text](https://github.com/OmdenaAI/Dryad/blob/task-3-gas-classification/DNN_Syed_Arsalan_Amin/encoded_specimen.png)
## **6. DagsHub Charts**
Here you can see the model comparisons.

![alt text](https://github.com/OmdenaAI/Dryad/blob/task-3-gas-classification/DNN_Syed_Arsalan_Amin/dagshub1.png)

And visual dashboard avaialable on [DagsHub](https://dagshub.com/Omdena/Dryad/experiments/#/experiment/m_36c104e845e54644b392265b1f6569c1) is as follows.

![alt text](https://github.com/OmdenaAI/Dryad/blob/task-3-gas-classification/DNN_Syed_Arsalan_Amin/dagshub_dashboard.png)
## **7. Models Comparison**
In this section you get a glimpse of the models comparison available on Dagshub.

![alt text](https://github.com/OmdenaAI/Dryad/blob/task-3-gas-classification/DNN_Syed_Arsalan_Amin/models_comparison.png)


## **8. Links**
For more detailed overview see my notebook on 
[Github](https://github.com/OmdenaAI/Dryad/blob/task-3-gas-classification/DNN_Syed_Arsalan_Amin/DNN_Syed_Arsalan_Amin_v1.ipynb.). \
And yes integrated mlflow code with :heart: on 
[DagsHub](https://dagshub.com/Omdena/Dryad/experiments/#/experiment/m_36c104e845e54644b392265b1f6569c1).