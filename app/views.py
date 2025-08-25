from flask import Blueprint, render_template, request
from flask_wtf import FlaskForm
from wtforms import DecimalField, SubmitField
import pandas as pd
import numpy as np
from scipy.spatial import distance as ds
from .initialize import app, estimator, song_names, song_cosines

# Define a blueprint
main = Blueprint('main', __name__)

# ig5music = pd.read_pickle('/Users/jenniferwang/musipy_by_jennwang/models/knn.pkl')
import os
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
big5music = pd.read_csv(os.path.join(BASE_DIR, 'data', 'final.csv'))

class PredictForm(FlaskForm):
    """Fields for Predict"""
    openness = DecimalField('Openness:', places=2)
    conscientiousness = DecimalField('Conscientiousness:', places=2)
    extraversion = DecimalField('Extraversion:', places=2)
    agreeableness = DecimalField('Agreeableness:', places=2)
    neuroticism = DecimalField('Neuroticism:', places=2)
    submit = SubmitField('Submit')

def get_distances(row, new_row):
    u = [row['ope'], row['agr'], row['neu'], row['con'], row['ext']]
    v = [new_row['ope'], new_row['agr'], new_row['neu'], new_row['con'], new_row['ext']]
    return ds.cosine(u, v)

@main.route('/', methods=('GET', 'POST'))
def index():
    """Index page"""
    form = PredictForm()
    song_returns = []

    if form.validate_on_submit():
        # Store the submitted values
        submitted_data = form.data
        print(submitted_data)

        # Extract only the relevant feature values and convert Decimal to float
        new_row = {
            'ope': float(submitted_data['openness']),
            'con': float(submitted_data['conscientiousness']),
            'ext': float(submitted_data['extraversion']),
            'agr': float(submitted_data['agreeableness']),
            'neu': float(submitted_data['neuroticism'])
        }

        # Calculate the cosine distances and add them to the DataFrame
        try:
            big5music['distance'] = big5music.apply(get_distances, args=(new_row,), axis=1)
            big5music_sorted = big5music.sort_values('distance')

            # Ensure the DataFrame contains the columns 'Title', 'Artist', 'Genre'
            # if ('Title' in big5music.columns):  #and 'Artist' in big5music.columns and 'Genre' in big5music.columns):
            #     song_returns = big5music_sorted[['Title']].head(5).values.tolist()
            #         #, 'Artist', 'Genre', 'distance']].head(5).values.tolist()
            #     print(song_returns)
            # else:
            #     print("The DataFrame does not contain the required columns.")
        except Exception as e:
            print(f"Error in calculating distances: {e}")

    return render_template('index.html', form=form, song_returns=song_returns)

@main.route('/recommend/')
def recommender():
    """Collaborative Filtering page"""
    selected_songs = request.args.get('selected_songs')
    all_songs = request.args.get('all_songs')
    scores = request.args.get('scores')

    if selected_songs and all_songs and scores:
        selected_songs = selected_songs.strip(';').split(';')
        all_songs = all_songs.strip(';').split(';')
        scores = scores.strip(';').split(';')

        try:
            a1 = song_cosines[selected_songs]

            recs_index = []
            recs_title = []
            recs_artist = []
            recs_genre = []

            for i in a1.columns:
                sorted_a1 = sorted(enumerate(a1[i]), key=lambda x: x[1], reverse=True)
                song_rec_index = [tup[0] for tup in sorted_a1[1:6]]
                recs_index.extend(song_rec_index)
                recs_title.append(song_names.Title.values[recs_index])
                recs_artist.append(song_names.Artist.values[recs_index])
                recs_genre.append(song_names.Genre.values[recs_index])

            newone = list(zip(recs_title[1], recs_artist[1], recs_genre[1]))
            print(newone)

            return render_template("recommend.html", song_returns=all_songs, newone=newone, scores=scores)
        except Exception as e:
            print(f"Error in recommender: {e}")

    return render_template("recommend.html", song_returns=[], newone=[], scores=[])
