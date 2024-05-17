import os
import pandas as pd
import joblib
from flask import Flask

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
