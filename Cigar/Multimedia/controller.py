from flask import request, jsonify, session, Blueprint
from flask_login import login_required
from flask_cors import  cross_origin

from Cigar.Multimedia.model import Category, Video, Book, Podcast, Motivation
from Cigar.Authentication.model import User

import random

multimedia = Blueprint('multimedia', __name__)


@cross_origin(supports_credentials=True)
@login_required
def get_media (mediaType=None):
    user = User.query.get (session['user_id'])

    if mediaType:
        if int (mediaType) == 1:
            media = Video.query.all()
            output = {'videos':Video.serialize_many(media), 'status':'OK'}
            return jsonify (output)

        elif int (mediaType) == 2:
            media = Book.query.all()
            output = {'books':Book.serialize_many(media), 'status':'OK'}
            return jsonify (output)

        elif int (mediaType) == 3:
            media = Podcast.query.all()
            output = {'podcasts':Podcast.serialize_many(media), 'status':'OK'}
            return jsonify (output)
    #show all multimedias
    else:
        motivations = Motivation.query.filter(~Motivation.id.in_ ([i.id for i in user.viewed_motivations]))
        output = {'motivations':Motivation.serialize_many(motivations) ,
                    'podcasts':Podcast.serialize_many(Podcast.query.all()),
                    'books':Book.serialize_many(Book.query.all()),
                    'videos':Video.serialize_many(Video.query.all()),
                    'status':'OK'}

multimedia.add_url_rule('/api/getMedia/<int:mediaType>' , view_func = get_media)


@cross_origin(supports_credentials=True)
@login_required
def get_motivation (count = 10):
    user = User.query.get (session['user_id'])

    all_motivations = Motivation.query.filter(~Motivation.id.in_ ([i.id for i in user.viewed_motivations]))
    selected_motivations = []
    random_range = random.sample (range(all_motivations.count()), 10)
    for idx in random_range:
        selected_motivations.append (all_motivations[idx])

    output = {'motivations':Motivation.serialize_many(selected_motivations), 'status':'OK'}
    return jsonify (output)

multimedia.add_url_rule('/api/getMotivation/<int:count>' , view_func = get_motivation)
