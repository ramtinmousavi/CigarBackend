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

        else:
            output = {'status':'wrong media type'}
            return jsonify (output)
    #show all multimedias
    else:
        output = {'podcasts':Podcast.serialize_many(Podcast.query.all()),
                    'books':Book.serialize_many(Book.query.all()),
                    'videos':Video.serialize_many(Video.query.all()),
                    'status':'OK'}
        return jsonify (output)

multimedia.add_url_rule('/api/getMedia/<int:mediaType>' , view_func = get_media)
multimedia.add_url_rule('/api/getMedia' , view_func = get_media)



@cross_origin(supports_credentials=True)
@login_required
def get_motivations (count = 10):
    user = User.query.get (session['user_id'])
    motivations = user.get_to_show_motivations()
    if int (count) != 10:
        motivations = motivations [:int(count)]
    output = {'motivations':Motivation.serialize_many(motivations), 'status':'OK'}
    return jsonify (output)

multimedia.add_url_rule('/api/getMotivations/<int:count>' , view_func = get_motivations)
multimedia.add_url_rule('/api/getMotivations' , view_func = get_motivations)


@cross_origin(supports_credentials=True)
@login_required
def get_media_by_category(categoryId, mediaType=None):
    category = Category.query.get (int(categoryId))
    if category:
        if mediaType:
            if int(mediaType) == 1:     #if video
                output = {'videos':Video.serialize_many(category.videos), 'status':'OK'}
                return jsonify (output)
            elif int(mediaType) == 2:   #if book
                output = {'books':Book.serialize_many(category.books), 'status':'OK'}
                return jsonify(output)
            elif int(mediaType) == 3:   #if podcast
                output = {'podcasts':Podcast.serialize_many(category.podcasts), 'status':'OK'}
                return jsonify (output)

            output = {'status':'wrong media type'}
            return jsonify (output)

        output = {'videos':Video.serialize_many(category.videos),
                    'books':Book.serialize_many(category.books),
                    'podcasts':Podcast.serialize_many(category.podcasts),
                    'status':'OK'}
        return jsonify (output)

    output = {'status':'wrong category id'}
    return jsonify (output)

multimedia.add_url_rule('/api/getMediaByCategory/<int:categoryId>/<int:mediaType>' , view_func = get_media_by_category)
multimedia.add_url_rule('/api/getMediaByCategory/<int:categoryId>' , view_func = get_media_by_category)
