from flask import Flask
from sklearn.externals import joblib
import pandas as pd


app = Flask(__name__)
app.config.from_object("app.config")

# unpickle my model
estimator = joblib.load('models/music.pkl')
song_names = pd.read_csv('data/songs_names.csv', encoding='utf-8')
song_cosines = pd.read_csv('data/song_cosines.csv')
target_names = ['setosa', 'versicolor', 'virginica']

from .views import *


# Handle Bad Requests
@app.errorhandler(404)
def page_not_found(e):
    """Page Not Found"""
    return render_template('404.html'), 404
