from flask import request, jsonify, session, Blueprint
from flask_login import login_required
from flask_cors import  cross_origin

from Cigar.Multimedia.model import Category, Video, Book, Podcast, Motivation
from Cigar.Authentication.model import User
from Cigar import response_generator

import random

multimedia = Blueprint('multimedia', __name__)


@cross_origin(supports_credentials=True)
@login_required
def get_media (mediaType=None):
    if mediaType:
        if int (mediaType) == 1:
            media = Video.query.all()
            output = response_generator (Video.serialize_many (media), 200, 'OK')
            return jsonify (output)

        elif int (mediaType) == 2:
            media = Book.query.all()
            output = response_generator (Book.serialize_many (media), 200, 'OK')
            return jsonify (output)

        elif int (mediaType) == 3:
            media = Podcast.query.all()
            output = response_generator (Podcast.serialize_many (media), 200, 'OK')
            return jsonify (output)

        else:
            output = response_generator (None, 406, 'wrong media type')
            return jsonify (output)
    #show all multimedias
    else:
        out = {'podcasts':Podcast.serialize_many(Podcast.query.all()),
                    'books':Book.serialize_many(Book.query.all()),
                    'videos':Video.serialize_many(Video.query.all()),
                    }
        output = response_generator (out, 200, 'OK')
        return jsonify (output)

multimedia.add_url_rule('/api/getMedia/<int:mediaType>' , view_func = get_media)
multimedia.add_url_rule('/api/getMedia' , view_func = get_media)



@cross_origin(supports_credentials=True)
@login_required
def get_motivations (subcategoryId):
    user = User.query.get (session['user_id'])
    motivations = user.get_to_show_motivations(subcategoryId)

    output = response_generator (Motivation.serialize_many (motivations), 200, 'OK')
    return jsonify (output)

multimedia.add_url_rule('/api/getMotivations/<int:subcategoryId>' , view_func = get_motivations)


@cross_origin(supports_credentials=True)
@login_required
def get_category (categoryId = None):
    if categoryId:
        category = Category.query.get(int(categoryId))
        if (category):
            output = response_generator (category.serialize_one(), 200, 'OK')
            return jsonify (output)

        output = response_generator (None, 406, 'wrong category id')
        return jsonify (output)

    categories = Category.query.all()
    output = response_generator (Category.serialize_many (categories), 200, 'OK')
    return jsonify (output)

multimedia.add_url_rule('/api/getCategory/<int:categoryId>' , view_func = get_category)
multimedia.add_url_rule('/api/getCategory' , view_func = get_category)
