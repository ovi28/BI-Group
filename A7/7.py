import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn
import nltk
import math
from sklearn import linear_model, metrics
from sklearn.model_selection import cross_val_score, KFold, cross_val_predict
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier
import folium
from folium.plugins import HeatMap


# Part 1

hackernews_items = pd.read_csv('hn_items.csv',delimiter=',',encoding='latin-1')

nltk.download('vader_lexicon')

from nltk.sentiment.vader import SentimentIntensityAnalyzer
model = SentimentIntensityAnalyzer()

hn_text = hackernews_items.dropna(subset=['text'], how='all')['text'].values

df = pd.DataFrame(columns=['text','neg','pos'])

data = []

for text in hn_text:
    score = model.polarity_scores(text)
    data.append({'text':text,'neg':score['neg'],'pos':score['pos']})
    
df = df.append(data)

df.head(5)

print('5 most positive: ')
print(df.nlargest(5,'pos'))

print('5 most negative: ')
print(df.nlargest(5,'neg'))

# Part 2

negatives = df['neg']
positives = df['pos']
    
folds = KFold(n_splits=10)
kmeans = KMeans(n_clusters=6)
classifier = KNeighborsClassifier()

X = negatives.values
Y = positives.values
XY = np.stack((X,Y),axis=1)

for train_idx, test_idx in folds.split(XY):
    idx = np.concatenate([train_idx,test_idx])
    XY_fold = XY[idx]
    
    kmeans.fit(XY_fold)
    labels = kmeans.labels_
    classifier.fit(XY_fold,labels)
    print(metrics.accuracy_score(labels, classifier.predict(XY_fold)))
    
    
# Part 3

boliga = pd.read_csv('boliga_zealand.csv').drop(['Index', '_1', 'Unnamed: 0'], axis=1)

zip_df = pd.DataFrame(boliga['zip_code'].str.split(' ',1).tolist(), columns = ['zip','city'])

boliga = boliga.assign(zip_int=zip_df['zip'])
boliga['zip_int'] = pd.to_numeric(boliga['zip_int'], errors='coerce')
boliga = boliga[boliga['zip_int'] < 3000]

heatmap_df = boliga[['lon','lat','price']].dropna()
boliga_map = folium.Map(location=[55.672103, 12.565529], zoom_start=10)

heat_data = [(e.lat,e.lon,float(e.price)) for e in heatmap_df.itertuples()]
HeatMap(heat_data, radius=7).add_to(boliga_map)
boliga_map.save('boliga_map.html')

#the best place to live in Copenhaga is around the Brønshøj-Rødovre area
#this places are have the cheapest housing market and relatively close to the central area