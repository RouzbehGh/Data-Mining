# -*- coding: utf-8 -*-
"""Implementation 3: Naïve Bayes Text Classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VHhO0IlIz_upR3SFqvhMYsAxLvgalg0m
"""

from google.colab import drive
drive.mount('/content/drive')

import os
import string
import numpy as np
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report

import pandas as pd
import numpy as np

train_data = pd.read_csv('/content/drive/My Drive/Data Mining/HW3/dataset/reviews_train.csv',error_bad_lines=False, usecols=['Review', 'Label'])
test_data = pd.read_csv('/content/drive/My Drive/Data Mining/HW3/dataset/reviews_test.csv', error_bad_lines=False, usecols=['Review', 'Label'])
train_data = train_data.dropna(axis = 0, how ='any') 
test_data = test_data.dropna(axis = 0, how ='any')

test_class_count = test_data['Label'].value_counts()
print('Negative:', test_class_count[0])
print('Positive:', test_class_count[1])
print('Proportion:', round(test_class_count[0] / test_class_count[1], 2), ': 1')

test_class_count.plot(kind='bar', title='Count (class)', color=['blue', 'red']);

train_class_count = train_data['Label'].value_counts()
print('Negative:', train_class_count[0])
print('Positive:', train_class_count[1])
print('Proportion:', round(train_class_count[0] / train_class_count[1], 2), ': 1')

train_class_count.plot(kind='bar', title='Count (class)', color=['blue', 'red']);

train_label = train_data['Label']
test_label = test_data['Label']
train_Review = train_data['Review']
test_Review = test_data['Review']

train_size = train_data.size
test_size = test_data.size

print("Amount of Train Data is :" ,train_size)
print("Amount of Test Data is :" ,test_size)

# Load Stop Words
stop_words = pd.read_csv('/content/drive/My Drive/Data Mining/HW3/dataset/sw.txt', header = None)

import nltk 
import string 
import re

import nltk
nltk.download('punkt')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer 
from nltk.stem.porter import PorterStemmer 
from nltk.tokenize import word_tokenize 
stemmer = PorterStemmer() 
lemmatizer = WordNetLemmatizer() 
  
def text_processing(text): 
    text = text.lower()
    text = re.sub(r'\d+', '', text) 
    translator = str.maketrans('', '', string.punctuation)
    text = text.translate(translator)
    text = " ".join(text.split())
    word_tokens = word_tokenize(text) 
    text = [word for word in word_tokens if word not in stop_words] 
    # provide context i.e. part-of-speech 
    text = [lemmatizer.lemmatize(word, pos ='v') for word in word_tokens] 
    return text
data = []
for i in range(179):
    data.append(text_processing(train_Review[i]))

data[1]

train_Review[1]

# Building a vocabulary of words from the given documents
vocab = {}
for i in range(len(train_Review)):
    word_list = []
    for word in train_Review[i][1].split():
        word_new  = word.strip(string.punctuation).lower()
        if (len(word_new)>2)  and (word_new not in stopwords):  
            if word_new in vocab:
                vocab[word_new]+=1
            else:
                vocab[word_new]=1

# Plotting a graph of no of words with a given frequency to decide cutoff drequency

num_words = [0 for i in range(max(train_Review.values())+1)] 
freq = [i for i in range(max(train_Review.values())+1)] 
for key in vocab:
    num_words[vocab[key]]+=1
plt.plot(freq,num_words)
plt.axis([1, 10, 0, 20000])
plt.xlabel("Frequency")
plt.ylabel("No of words")
plt.grid()
plt.show()

cutoff_freq = 80
# For deciding cutoff frequency
num_words_above_cutoff = len(vocab)-sum(num_words[0:cutoff_freq]) 
print("Number of words with frequency higher than cutoff frequency({}) :".format(cutoff_freq),num_words_above_cutoff)

# Words with frequency higher than cutoff frequency are chosen as features
# (i.e we remove words with low frequencies as they would not be significant )
features = []
for key in vocab:
    if vocab[key] >=cutoff_freq:
        features.append(key)

# To represent test data as word vector counts
test_Review_dataset = np.zeros((len(test_Review),len(features)))
# This can take some time to complete
for i in range(len(test_Review)):
    # print(i) # Uncomment to see progress
    word_list = [ word.strip(string.punctuation).lower() for word in test_Review[i][1].split()]
    for word in word_list:
        if word in features:
           test_Review_dataset[i][features.index(word)] += 1

# Using sklearn's Multinomial Naive Bayes
clf = MultinomialNB()
clf.fit(X_train_dataset,test_label)
test_label_pred = clf.predict(test_Review_dataset)
sklearn_score_train = clf.score(train_Review_dataset,train_label)
print("Sklearn's score on training data :",sklearn_score_train)
sklearn_score_test = clf.score(test_Review_dataset,test_label)
print("Sklearn's score on testing data :",sklearn_score_test)
print("Classification report for testing data :-")
print(classification_report(test_label, test_label_pred))

# Implementing Multinomial Naive Bayes from scratch
class MultinomialNaiveBayes:
    
    def __init__(self):
        # count is a dictionary which stores several dictionaries corresponding to each news category
        # each value in the subdictionary represents the freq of the key corresponding to that news category 
        self.count = {}
        # classes represents the different news categories
        self.classes = None
    
    def fit(self,train_Review,test_re):
        # This can take some time to complete       
        self.classes = set(train_label)
        for class_ in self.classes:
            self.count[class_] = {}
            for i in range(len(train_Review[0])):
                self.count[class_][i] = 0
            self.count[class_]['total'] = 0
            self.count[class_]['total_points'] = 0
        self.count['total_points'] = len(train_Review)
        
        for i in range(len(train_Review)):
            for j in range(len(train_Review[0])):
                self.count[train_label[i]][j]+=train_Review[i][j]
                self.count[train_label[i]]['total']+=train_Review[i][j]
            self.count[train_label[i]]['total_points']+=1
    
    def __probability(self,test_point,class_):
        
        log_prob = np.log(self.count[class_]['total_points']) - np.log(self.count['total_points'])
        total_words = len(test_point)
        for i in range(len(test_point)):
            current_word_prob = test_point[i]*(np.log(self.count[class_][i]+1)-np.log(self.count[class_]['total']+total_words))
            log_prob += current_word_prob
        
        return log_prob
    
    
    def __predictSinglePoint(self,test_point):
        
        best_class = None
        best_prob = None
        first_run = True
        
        for class_ in self.classes:
            log_probability_current_class = self.__probability(test_point,class_)
            if (first_run) or (log_probability_current_class > best_prob) :
                best_class = class_
                best_prob = log_probability_current_class
                first_run = False
                
        return best_class
        
  
    def predict(self,X_test):
        # This can take some time to complete
        Y_pred = [] 
        for i in range(len(X_test)):
        # print(i) # Uncomment to see progress
            Y_pred.append( self.__predictSinglePoint(X_test[i]) )
        
        return Y_pred
    
    def score(self,Y_pred,Y_true):
        # returns the mean accuracy
        count = 0
        for i in range(len(Y_pred)):
            if Y_pred[i] == Y_true[i]:
                count+=1
        return count/len(Y_pred)

clf2 = MultinomialNaiveBayes()
clf2.fit(X_train_dataset,train_label)
test_label_pred = clf2.predict(test_Review_dataset)
our_score_test = clf2.score(test_label_pred,test_label)  
print("Our score on testing data :",our_score_test)
print("Classification report for testing data :-")
print(classification_report(test_label, test_label_pred))

print("Score of inbuilt sklearn's MultinomialNB on the same data :",sklearn_score_test)