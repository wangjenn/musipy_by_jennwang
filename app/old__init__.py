from flask import Flask, render_template
import joblib
import numpy as np
import pandas as pd
import os
from .views import main as main_blueprint

app = Flask(__name__)
app.config.from_object("app.config.Config")

# Define the base directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define file paths
MODEL_PATH = os.path.join(BASE_DIR, '../models/knn.pkl')
SONG_NAMES_PATH = os.path.join(BASE_DIR, '../data/songs_names.csv')
SONG_COSINES_PATH = os.path.join(BASE_DIR, '../data/song_cosines.csv')

# Unpickle the model
try:
    estimator = joblib.load(MODEL_PATH)
    print("Model loaded successfully.")
except FileNotFoundError:
    estimator = None
    print("Model file not found.")
except ModuleNotFoundError as e:
    estimator = None
    print(f"Module not found error: {e}")

# Load CSV files
try:
    song_names = pd.read_csv(SONG_NAMES_PATH, encoding='utf-8')
    print("Songs names CSV file loaded successfully.")
except FileNotFoundError:
    song_names = None
    print("Songs names CSV file not found.")

try:
    song_cosines = pd.read_csv(SONG_COSINES_PATH)
    print("Song cosines CSV file loaded successfully.")
except FileNotFoundError:
    song_cosines = None
    print("Song cosines CSV file not found.")


app.register_blueprint(main_blueprint)
# from .views import *


# Handle Bad Requests
@app.errorhandler(404)
def page_not_found(e):
    """Page Not Found"""
    return render_template('404.html'), 404


# from flask import Flask, render_template
# import os as os
# import joblib
# import pandas as pd
#
# app = Flask(__name__)
# app.config.from_object("app.config.Config")
#
# # Define the base directory (newly added)
# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
#
# # Define file paths (newly added)
# MODEL_PATH = os.path.join(BASE_DIR, '../models/music.pkl')
# SONG_NAMES_PATH = os.path.join(BASE_DIR, '../data/songs_names.csv')
# SONG_COSINES_PATH = os.path.join(BASE_DIR, '../data/song_cosines.csv')
#
# # Unpickle the model
# try:
#     estimator = joblib.load('models/music.pkl')
# except FileNotFoundError:
#     estimator = None
#     print("Model file not found.")
#
# # Load CSV files
# try:
#     song_names = pd.read_csv('data/songs_names.csv', encoding='utf-8')
# except FileNotFoundError:
#     song_names = None
#     print("Songs names CSV file not found.")
#
# try:
#     song_cosines = pd.read_csv('data/song_cosines.csv')
# except FileNotFoundError:
#     song_cosines = None
#     print("Song cosines CSV file not found.")
#
# target_names = ['setosa', 'versicolor', 'virginica']
# # Handle Bad Requests
# @app.errorhandler(404)
# def page_not_found(e):
#     """Page Not Found"""
#     return render_template('404.html'), 404
#
#
#
#
#
# # from flask import Flask
# # import joblib
# # import pandas as pd
# #
# #
# # app = Flask(__name__)
# # app.config.from_object("app.config")
# #
# # # unpickle my model
# # estimator = joblib.load('models/music.pkl')
# # song_names = pd.read_csv('data/songs_names.csv', encoding='utf-8')
# # song_cosines = pd.read_csv('data/song_cosines.csv')
# # target_names = ['setosa', 'versicolor', 'virginica']
# #
# #
# #
# # # Handle Bad Requests
# # @app.errorhandler(404)
# # def page_not_found(e):
# #     """Page Not Found"""
# #     return render_template('404.html'), 404
