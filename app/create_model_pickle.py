import joblib
import pandas as pd
import sklearn
from sklearn import model_selection, neighbors
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error
from scipy.spatial import distance as ds
import numpy as np
import statsmodels as sms
import scipy.stats as stats
import os

big5music = pd.read_csv('/Users/jenniferwang/musipy_by_jennwang/data/big5_music_fixed.csv')
big5music


def get_distances(row, new_row):
    u = [row['ope'], row['agr'], row['neu'], row['con'], row['ext']]
    v = [new_row['ope'], new_row['agr'], new_row['neu'], new_row['con'], new_row['ext']]
    return ds.cosine(u, v)


# Define X and y

"""
X = Personality Dimensions 
Y = Ratings of the songs 
"""

feature_columns = ['ope', 'con', 'ext', 'agr', 'neu']
X = big5music[feature_columns]

target_columns = [f'q{i}' for i in range(1, 51)]
y = big5music[target_columns]

knn = KNeighborsRegressor(n_neighbors=2000, weights='distance', n_jobs=-1)
knn.fit(X, y)

knn.score(X, y)

# save as pickle!
joblib.dump(knn, 'knn.pkl')
