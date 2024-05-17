from flask import Blueprint, render_template, request
from flask_wtf import FlaskForm
from wtforms import DecimalField, SubmitField
import pandas as pd
import numpy as np
from scipy.spatial import distance as ds
from .initialize import app, estimator, song_names, song_cosines

# Define blueprint
main = Blueprint('main', __name__)

class PredictForm(FlaskForm):
    """Fields for Predict"""
    openness = DecimalField('Openness:', places=2)
    conscientiousness = DecimalField('Conscientiousness:', places=2)
    extraversion = DecimalField('Extraversion:', places=2)
    agreeableness = DecimalField('Agreeableness:', places=2)
    neuroticism = DecimalField('Neuroticism:', places=2)
    submit = SubmitField('Submit')

big5music = Blueprint('big5music', __name__)

def get_distances(row, new_row):
    u = [row['ope'], row['agr'], row['neu'], row['con'], row['ext']]
    v = [new_row['ope'], new_row['agr'], new_row['neu'], new_row['con'], new_row['ext']]
    return ds.cosine(u,v)

# @app.route('/', methods=('GET', 'POST'))
@main.route('/', methods=('GET', 'POST'))
def index():
    """Index page"""
    form = PredictForm()
    song_returns = []

    if form.validate_on_submit():
        # store the submitted values
        submitted_data = form.data
        print(submitted_data)

        # Extract only the relevant feature values
        # features = [

        new_row = {
            'ope': float(submitted_data['openness']),
            'con': float(submitted_data['conscientiousness']),
            'ext': float(submitted_data['extraversion']),
            'agr': float(submitted_data['agreeableness']),
            'neu': float(submitted_data['neuroticism'])
        }


        # new_row = [submitted_data['openness'],
        #     submitted_data['conscientiousness'],
        #     submitted_data['extraversion'],
        #     submitted_data['agreeableness'],
        #     submitted_data['neuroticism']
        # ]

        ## Convert Decimal to float
        # new_row = [float(f) for f in new_row]
        # get_distances(submitted_data, new_row)
       # features = [float(f) for f in features]

        # Create array from values
        try:
            big5music['distance'] = big5music.apply(get_distances, args=(new_row,), axis=1)
            big5music_sorted = big5music.sort_values('distance')

            # song_returns = big5music_sorted[['Title', 'Artist', 'Genre', 'distance']].head(5).values.tolist()
            # print(song_returns)
            # # content_songs = estimator.predict(np.array([features]))
            # song_recs = song_names.copy()
            # # song_recs['Rating'] = content_songs
            # song_recs = song_recs.sort_values('Rating', ascending=False)
            # song_returns = [tuple(x) for x in song_recs[["Title", "Artist", "Genre"]].values][0:5]
            # print(song_returns)


            # Ensure the DataFrame contains the columns 'Title', 'Artist', 'Genre' #
            if 'Title' in big5music.columns and 'Artist' in big5music.columns and 'Genre' in big5music.columns:
                song_returns = big5music_sorted[['Title', 'Artist', 'Genre', 'distance']].head(5).values.tolist()
                print(song_returns)
            else:
                print("The DataFrame does not contain the required columns.")
            # if estimator is not None:
            #     # content_songs = estimator.predict(np.array([features]))
            #     song_recs = song_names.copy()
            #     # song_recs['Rating'] = content_songs
            #     song_recs = song_recs.sort_values('Rating', ascending=False)
            #     song_returns = [tuple(x) for x in song_recs[["Title", "Artist", "Genre"]].values][0:5]
            #     print(song_returns)
            # else:
            #     print("Estimator is not loaded properly.")
        except Exception as e:
            print(f"Error in calculating distance: {e}")

    return render_template('index.html', form=form, song_returns=song_returns)

# @app.route('/recommend/')
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

# if __name__ == '__main__':
#     app.run(debug=True)

# from flask import render_template, request
# from flask_wtf import Form
# from wtforms import fields
# from app import app, estimator, song_names, song_cosines
# # target_names
# # from wtforms.validators import Required
# import numpy as np
#
#
# class PredictForm(Form):
#     """Fields for Predict"""
#     myChoices = ["one", "two", "three"]
#     openness = fields.DecimalField('Openness:', places=2)
#                                    # validators=[Required()])
#     conscientiousness = fields.DecimalField('Conscientiousness:', places=2)
#     #validators=[Required()])
#     extraversion = fields.DecimalField('Extraversion:', places=2)
#                                        #validators=[Required()])
#     agreeableness = fields.DecimalField('Agreeableness:', places=2)
#                                         #validators=[Required()])
#     neuroticism = fields.DecimalField('Neuroticism:', places=2)
#     #validators=[Required()])
#
#     submit = fields.SubmitField('Submit')
#
#     def validate_on_submit(self):
#         pass
#
#
# @app.route('/', methods=('GET', 'POST'))
# def index():
#     """Index page"""
#     form = PredictForm()
#     print("Here")
#
#     song_returns = []
#     # always have empty dictionary
#     data_point = {}
#
#     if form.validate_on_submit():
#         # store the submitted values
#         submitted_data = form.data
#         print(submitted_data)
#
#         # Retrieve values from form
#         openness = submitted_data['openness']
#         conscientiousness = submitted_data['conscientiousness']
#         extraversion = submitted_data['extraversion']
#         agreeableness = submitted_data['agreeableness']
#         neuroticism = submitted_data['neuroticism']
#
#         # Create array from values// here is where to put the FUNCTION
#         content_songs = estimator.predict(np.array([openness, conscientiousness, extraversion, agreeableness, neuroticism])).transpose()
#         song_recs = song_names.copy()
#         song_recs['Rating'] = content_songs
#         song_recs = song_recs.sort('Rating', ascending=False)
#         ## CHANGE THIS to add AUDIO##
#         song_returns = [tuple(x) for x in song_recs[["Title", "Artist", "Genre"]].values][0:5]
#         print(song_returns)
#
#    # added a new dictionary, then passed it to HTML
#     # add data_point
#     return render_template('index.html',
#         form=form,
#         song_returns=song_returns)
#
# # app for collaborative filtering
#
# @app.route('/recommend/')
# def recommender():
#     """Collaborative Filtering page"""
#     recommended_songs = []
#     selected_songs = request.args['selected_songs']
#     all_songs = request.args['all_songs']
#     scores = request.args['scores']
#
#     selected_songs = selected_songs.strip(';').split(';')
#     all_songs = all_songs.strip(';').split(';')
#     scores = scores.strip(';').split(';')
#
#     a1 = song_cosines.filter(items=selected_songs)
#
#     recs_index = []
#     recs_title = []
#     recs_artist=[]
#     recs_genre =[]
#     print('in Recommender')
#     for i in a1.columns:
#         sorted_a1 = sorted(enumerate(a1[i]),key=lambda x:x[1],reverse=True)
#         song_rec_index = [tup[0] for tup in sorted_a1[1:6]]
#         recs_index.extend(song_rec_index)
#         recs_title.append(song_names.Title.values[recs_index])
#         recs_artist.append(song_names.Artist.values[recs_index])
#         recs_genre.append(song_names.Genre.values[recs_index])
#         ## CHANGE HERE!!!
#     newone = list(zip(recs_title[1], recs_artist[1], recs_genre[1]))
#     print(newone)
#
#     return render_template("recommend.html", song_returns=all_songs, newone=newone, scores=scores)
