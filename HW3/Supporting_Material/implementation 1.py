# -*- coding: utf-8 -*-
"""Implementation 1: Decision Tree.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XbKeP2FDOsGt5y70Croj9D9FNDHwX2_4
"""

from google.colab import drive
drive.mount('/content/drive')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('/content/drive/My Drive/Data Mining/HW3/dataset/heart.csv')

data.head()

del data['Unnamed: 0']

data.head()

data.info()

print("The oldest person in our dataset is :" , data['age'].max())

def change_ages(age):
    if(0<= age <= 10):
        return 0
    elif ((11<= age <= 20)):
        return 1
    elif ((21<= age <= 30)):
        return 2
    elif ((31<= age <= 40)):
        return 3
    elif ((41<= age <= 50)):
        return 4
    elif ((51<= age <= 60)):
        return 5
    elif ((61<= age <= 70)):
        return 6
    elif ((71<= age <= 80)):
        return 7
data['age'] = data.age.apply(change_ages)

data.head()

data.sex = data.sex.astype('category')
data.cp = data.cp.astype('category')
data.fbs = data.fbs.astype('category')
data.exang = data.exang.astype('category')
data.thal = data.thal.astype('category')
data.target = data.target.astype('category')

dummies = pd.get_dummies(data = data , drop_first= True)
dummies.head()

dummies.tail()

dummies.info()

from sklearn.preprocessing import StandardScaler
std_scaler = StandardScaler()
std_scaler.fit(dummies.drop('target_yes',axis=1))

scaled_features = std_scaler.transform(dummies.drop('target_yes',axis=1))

colms = dummies.columns.delete(5)
X = pd.DataFrame(scaled_features,columns=colms)
y = dummies['target_yes']

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score 
from sklearn.ensemble import RandomForestClassifier


from sklearn.tree import export_graphviz
from sklearn.datasets import load_wine
from IPython.display import SVG
from graphviz import Source
from IPython.display import display

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

"""**Decision Tree with gini**"""

dtree_gini = DecisionTreeClassifier(criterion='gini')
cls = dtree_gini.fit(X_train,y_train)
y_pred = cls.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

export_graphviz(dtree_gini, out_file="/content/drive/My Drive/Data Mining/HW3/dataset/dtree_gini.dot",
                feature_names=X_train.columns,
                filled = True)

"""**Decision Tree with entropy**"""

dtree_entropy = DecisionTreeClassifier(criterion='entropy')
cls = dtree_entropy.fit(X_train,y_train)
y_pred = cls.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

export_graphviz(dtree_entropy, out_file="/content/drive/My Drive/Data Mining/HW3/dataset/dtree_entropy.dot",
                feature_names=X_train.columns,
                filled = True)

"""**Random Forest with gini**"""

rf_gini = RandomForestClassifier(n_jobs=-1, n_estimators=50, criterion='gini')
rf_model = rf_gini.fit(X_train, y_train)
y_pred = rf_model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

export_graphviz(rf_gini.estimators_[0], out_file="/content/drive/My Drive/Data Mining/HW3/dataset/rf_gini.dot",
                feature_names=X_train.columns,
                filled = True)

"""**Random Forest with entropy**"""

rf_entropy = RandomForestClassifier(n_jobs=-1, n_estimators=50, criterion='entropy')
rf_model = rf_entropy.fit(X_train, y_train)
y_pred = rf_model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

export_graphviz(rf_entropy.estimators_[0], out_file="/content/drive/My Drive/Data Mining/HW3/dataset/rf_entropy.dot",
                feature_names=X_train.columns,
                filled = True)

graph = Source(export_graphviz(dtree_gini, out_file=None,
                                    feature_names=X_train.columns,
                                    filled = True))
display(SVG(graph.pipe(format='svg')))

graph = Source(export_graphviz(dtree_entropy, out_file=None,
                                    feature_names=X_train.columns,
                                    filled = True))
display(SVG(graph.pipe(format='svg')))

graph = Source(export_graphviz(rf_gini.estimators_[0], out_file=None,
                                    feature_names=X_train.columns,
                                    filled = True))
display(SVG(graph.pipe(format='svg')))

graph = Source(export_graphviz(rf_entropy.estimators_[0], out_file=None,
                                    feature_names=X_train.columns,
                                    filled = True))
display(SVG(graph.pipe(format='svg')))

param = {'min_samples_split': [2, 5, 10],
        'max_depth': [5, 10, 15, None]}

"""**grid search on decision tree with gini**"""

gs1 = GridSearchCV(dtree_gini, param, cv=5,
                   n_jobs=-1, iid=True,
                   return_train_score=True)
gs_fit1 = gs1.fit(X, y)
pd.DataFrame(gs_fit1.cv_results_).sort_values('mean_test_score',
                                             ascending=False)[0:5]

"""**grid search on decision tree with entropy**"""

gs2 = GridSearchCV(dtree_entropy, param, cv=5,
                   n_jobs=-1, iid=True,
                   return_train_score=True)
gs_fit2 = gs2.fit(X, y)
pd.DataFrame(gs_fit2.cv_results_).sort_values('mean_test_score',
                                             ascending=False)[0:5]

"""**grid search on random forest with gini**"""

gs3 = GridSearchCV(rf_gini, param, cv=5,
                   n_jobs=-1, iid=True,
                   return_train_score=True)
gs_fit3 = gs3.fit(X, y)
pd.DataFrame(gs_fit3.cv_results_).sort_values('mean_test_score',
                                             ascending=False)[0:5]

"""**grid search on random forest with entropy**"""

gs4 = GridSearchCV(rf_entropy, param, cv=5,
                   n_jobs=-1, iid=True,
                   return_train_score=True)
gs_fit4 = gs4.fit(X, y)
pd.DataFrame(gs_fit4.cv_results_).sort_values('mean_test_score',
                                             ascending=False)[0:5]

from sklearn.tree import DecisionTreeClassifier
dtree = DecisionTreeClassifier()

dtree.fit(X_train,y_train)

y_pred = dtree.predict(X_test)

from sklearn.metrics import confusion_matrix,classification_report

print(classification_report(y_test,y_pred))