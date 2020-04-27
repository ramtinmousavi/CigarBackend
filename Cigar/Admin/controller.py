from flask import request, jsonify, session, Blueprint
from flask_login import login_required
from flask_cors import  cross_origin

#import models from Admin or other packages
from Cigar.Authentication.model import User
from Cigar.Multimedia.model import Category, Book, Video, Podcast, Motivation

admin = Blueprint('admin', __name__)


class Admin_Required:
    def __init__ (self, params):
        self.params = params

    def __call__ (self, f):

        def wrapped_f ():
            if session ['role'] == 'admin':
                return f()
            else:
                out = {}
                for param in self.params :
                    out [param] = ''
                out ['status'] = 'access denied'

                return jsonify (out)
        wrapped_f.__name__ = f.__name__
        return wrapped_f


@cross_origin(supports_credentials=True)
@login_required
@Admin_Required (['motivation'])
def add_motivation (categoryId):
    if request.method == 'POST':
        req = request.get_json(force = True)

        title = req['title']
        description = req['description']
        new_motivation = Motivation (title, description, int(categoryId))
        new_motivation.save()

        output = {'motivation':new_motivation.serialize_one(), 'status':'OK'}
        return jsonify (output)

    output = {'motivation':'', 'status':'method is not POST'}
    return jsonify (output)

admin.add_url_rule('/api/addMotivation/<int:categoryId>' , view_func = add_motivation, methods = ['POST' , 'GET'])


@cross_origin(supports_credentials=True)
@login_required
@Admin_Required (['motivation'])
def edit_motivation (motivationId):
    if request.method == 'POST':
        req = request.get_json(force = True)

        current_motivation = Motivation.query.get (int(motivationId))
        if (current_motivation is not None):

            title = req['title']
            description = req['description']
            current_motivation.edit (title, description)

            output = {'motivation':current_motivation.serialize_one(), 'status':'OK'}
            return jsonify (output)

        output = {'motivation':'', 'status':'motivation id is wrong'}
        return jsonify (output)

    output = {'motivation':'', 'status':'method is not POST'}
    return jsonify (output)

admin.add_url_rule('/api/editMotivation/<int:motivationId>' , view_func = edit_motivation, methods = ['POST' , 'GET'])


@cross_origin(supports_credentials=True)
@login_required
@Admin_Required ([])
def delete_motivation (motivationId):

    current_motivation = Motivation.query.get (int(motivationId))
    if (current_motivation is not None):
        current_motivation.delete()
        output = {'status':'OK'}
        return jsonify (output)

    output = {'status':'motivation id is wrong'}
    return jsonify (output)

admin.add_url_rule('/api/deleteMotivation/<int:motivationId>' , view_func = delete_motivation)


@cross_origin(supports_credentials=True)
@login_required
@Admin_Required (['motivation'])
def get_motivation (motivationId):

    current_motivation = Motivation.query.get (int(motivationId))
    if (current_motivation is not None):

        output = {'motivation':current_motivation.serialize_one(), 'status':'OK'}
        return jsonify (output)

    output = {'motivation':'', 'status':'motivation id is wrong'}
    return jsonify (output)


admin.add_url_rule('/api/getMotivation/<int:motivationId>' , view_func = get_motivation)


@cross_origin(supports_credentials=True)
@login_required
@Admin_Required (['motivations'])
def get_all_motivations ():

    motivations = Motivation.query.all()

    output = {'motivations': Motivation.serialize_many(motivations), 'status':'OK'}

admin.add_url_rule('/api/getAllMotivations/' , view_func = get_all_motivations)

#------------------------------------------------------#

@cross_origin(supports_credentials=True)
@login_required
@Admin_Required (['video'])
def add_video (categoryId):
    if request.method == 'POST':
        req = request.get_json(force = True)

        title = req['title']
        description = req['description']
        url = req['url']
        new_video = Video (title, description, utrl, int(categoryId))
        new_video.save()

        output = {'video':new_video.serialize_one(), 'status':'OK'}
        return jsonify (output)

    output = {'motivation':'', 'status':'method is not POST'}
    return jsonify (output)

admin.add_url_rule('/api/addVideo/<int:categoryId>' , view_func = add_video, methods = ['POST' , 'GET'])


@cross_origin(supports_credentials=True)
@login_required
@Admin_Required (['video'])
def edit_video (videoId):
    if request.method == 'POST':
        req = request.get_json(force = True)

        current_video = Video.query.get (int(videoId))
        if (current_video is not None):

            title = req['title']
            description = req['description']
            url = req ['url']
            current_video.edit (title, description, url)

            output = {'video':current_video.serialize_one(), 'status':'OK'}
            return jsonify (output)

        output = {'video':'', 'status':'video id is wrong'}
        return jsonify (output)

    output = {'video':'', 'status':'method is not POST'}
    return jsonify (output)

admin.add_url_rule('/api/editVideo/<int:videoId>' , view_func = edit_video, methods = ['POST' , 'GET'])


@cross_origin(supports_credentials=True)
@login_required
@Admin_Required ([])
def delete_video (videoId):

    current_video = Video.query.get (int(videoId))
    if (current_video is not None):
        current_video.delete()
        output = {'status':'OK'}
        return jsonify (output)

    output = {'status':'video id is wrong'}
    return jsonify (output)

admin.add_url_rule('/api/deleteVideo/<int:videoId>' , view_func = delete_video)


@cross_origin(supports_credentials=True)
@login_required
@Admin_Required (['video'])
def get_motivation (videoId):

    current_video = Video.query.get (int(videoId))
    if (current_video is not None):

        output = {'video':current_video.serialize_one(), 'status':'OK'}
        return jsonify (output)

    output = {'video':'', 'status':'video id is wrong'}
    return jsonify (output)


admin.add_url_rule('/api/getVideo/<int:videoId>' , view_func = get_video)


@cross_origin(supports_credentials=True)
@login_required
@Admin_Required (['videos'])
def get_all_videos ():

    videos = Video.query.all()

    output = {'videos': Video.serialize_many(videos), 'status':'OK'}

admin.add_url_rule('/api/getAllVideos/' , view_func = get_all_videos)
