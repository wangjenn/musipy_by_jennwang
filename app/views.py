
from flask import render_template, request
from flask_wtf import Form
from wtforms import fields
from wtforms.validators import Required
import pandas as pd
import numpy as np
import csv
from . import app, estimator, target_names, song_names, song_cosines


class PredictForm(Form):
    """Fields for Predict"""
    myChoices = ["one", "two", "three"]
    openness = fields.DecimalField('Openness:', places=2, validators=[Required()])
    conscientiousness = fields.DecimalField('Conscientiousness:', places=2, validators=[Required()])
    extraversion = fields.DecimalField('Extraversion:', places=2, validators=[Required()])
    agreeableness = fields.DecimalField('Agreeableness:', places=2, validators=[Required()])
    neuroticism = fields.DecimalField('Neuroticism:', places=2, validators=[Required()])

    submit = fields.SubmitField('Submit')


@app.route('/', methods=('GET', 'POST'))
def index():
    """Index page"""
    form = PredictForm()
    print("Here")

    song_returns = []
    # always have empty dictionary 
    data_point = {}

    if form.validate_on_submit():
        # store the submitted values
        submitted_data = form.data
        print(submitted_data)

        # Retrieve values from form
        openness = submitted_data['openness']
        conscientiousness = submitted_data['conscientiousness']
        extraversion = submitted_data['extraversion']
        agreeableness = submitted_data['agreeableness']
        neuroticism = submitted_data['neuroticism']

        # Create array from values// here is where to put the FUNCTION
        content_songs = estimator.predict(np.array([openness, conscientiousness, extraversion, agreeableness, neuroticism])).transpose()
        song_recs = song_names.copy()
        song_recs['Rating'] = content_songs
        song_recs = song_recs.sort('Rating', ascending=False)
        ## CHANGE THIS to add AUDIO## 
        song_returns = [tuple(x) for x in song_recs[["Title", "Artist", "Genre"]].values][0:5]
        print(song_returns)


   # added a new dictionary, then passed it to HTML 
    # add data_point 
    return render_template('index.html',
        form=form,
        song_returns=song_returns)

# app for collaborative filtering 

@app.route('/recommend/')
def Recommneder():
    """Collaborative Filtering page"""
    recommended_songs = []
    selected_songs = request.args['selected_songs']
    all_songs = request.args['all_songs']
    scores = request.args['scores']

    selected_songs = selected_songs.strip(';').split(';')
    all_songs = all_songs.strip(';').split(';')
    scores = scores.strip(';').split(';')

    a1 = song_cosines.filter(items=selected_songs)

    recs_index = []
    recs_title = []
    recs_artist=[]
    recs_genre =[]
    print('in Recommender')
    for i in a1.columns: 
        sorted_a1 = sorted(enumerate(a1[i]),key=lambda x:x[1],reverse=True)
        song_rec_index = [tup[0] for tup in sorted_a1[1:6]]
        recs_index.extend(song_rec_index)
        recs_title.append(song_names.Title.values[recs_index])
        recs_artist.append(song_names.Artist.values[recs_index])
        recs_genre.append(song_names.Genre.values[recs_index]) 
        ## CHANGE HERE!!!
    newone = list(zip(recs_title[1], recs_artist[1], recs_genre[1]))
    print(newone)

    return render_template("recommend.html", song_returns=all_songs, newone = newone, scores=scores)    


