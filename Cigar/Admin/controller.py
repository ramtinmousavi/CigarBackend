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

        output = {'motivation':Motivation.serialize_one(new_motivation), 'status':'OK'}
        return jsonify (output)

    output = {'motivation':'', 'status':'method is not POST'}
    return jsonify (output)

admin.add_url_rule('/api/addMotivation/<int:categoryId>' , view_func = add_motivation)


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

            output = {'motivation':Motivation.serialize_one(current_motivation), 'status':'OK'}
            return jsonify (output)

        output = {'motivation':'', 'status':'motivation id is wrong'}
        return jsonify (output)

    output = {'motivation':'', 'status':'method is not POST'}
    return jsonify (output)

admin.add_url_rule('/api/editMotivation/<int:motivationId>' , view_func = edit_motivation)


@cross_origin(supports_credentials=True)
@login_required
@Admin_Required (['motivation'])
def delete_motivation (motivationId):
    if request.method == 'POST':
        req = request.get_json(force = True)

        current_motivation = Motivation.query.get (int(motivationId))
        if (current_motivation is not None):
            current_motivation.delete()
            output = {'motivation':'', 'status':'OK'}
            return jsonify (output)

        output = {'motivation':'', 'status':'motivation id is wrong'}
        return jsonify (output)

    output = {'motivation':'', 'status':'method is not POST'}
    return jsonify (output)

admin.add_url_rule('/api/deleteMotivation/<int:motivationId>' , view_func = delete_motivation)


@cross_origin(supports_credentials=True)
@login_required
@Admin_Required (['motivation'])
def get_motivation (motivationId):
    if request.method == 'POST':
        req = request.get_json(force = True)

        current_motivation = Motivation.query.get (int(motivationId))
        if (current_motivation is not None):

            output = {'motivation':Motivation.serialize_one(current_motivation), 'status':'OK'}
            return jsonify (output)

        output = {'motivation':'', 'status':'motivation id is wrong'}
        return jsonify (output)

    output = {'motivation':'', 'status':'method is not POST'}
    return jsonify (output)

admin.add_url_rule('/api/getMotivation/<int:motivationId>' , view_func = get_motivation)
