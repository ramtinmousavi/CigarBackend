from flask import request, jsonify, session, Blueprint
from flask_login import login_required
from flask_cors import  cross_origin

from Cigar.Multimedia.model import Video, Book, Podcast
from Cigar import response_generator


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
