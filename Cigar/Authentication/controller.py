from flask import request, jsonify, session, Blueprint
from flask_login import login_required, login_user, logout_user
from flask_cors import  cross_origin

from Cigar.Authentication.model import User

import re

authentication = Blueprint('authentication', __name__)


@cross_origin(support_credentials=True)
def sign_up():
    if request.method == 'POST':
        req = request.get_json(force = True)

        name = req['name']
        email = req ['email']
        password = req ['password']

        if (re.search ('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$', email)):

            if (User.query_by_email (email) is not None):
                output = {'user':'', 'status':'user already exists'}
                return jsonify (output)

            new_user = User (name, email, password)
            new_user.save()

            output = {'user':new_user.serialize_one(), 'status':'OK'}
            return jsonify (output)

        output = {'user':'', 'status':'wrong email format'}
        return jsonify(output)

    output = {'user':'', 'status':'method is not POST'}
    return jsonify (output)

authentication.add_url_rule('/api/signup' , view_func = sign_up, methods = ['POST' , 'GET'])


@cross_origin(support_credentials=True)
def login():
    if request.method == 'POST':
        req = request.get_json(force = True)

        email = req['email']
        password = req ['password']

        stored_user = User.query_by_email (email)
        if (stored_user is not None) and (stored_user.check_password(password)):
            login_user(stored_user)
            session ['user_id'] = stored_user.id
            session ['role'] = stored_user.role

            output = {'user': stored_user.serialize_one(), 'status':'OK'}
            return jsonify (output)

        else:
            if stored_user is None:
                output = {'user':'', 'status':'user not found'}
                return jsonify (output)
            elif not stored_user.check_password(req['password']):
                output = {'user':'', 'status':'password incorrect'}
                return jsonify(output)

    output = {'user':'', 'status':'method is not POST'}
    return jsonify (output)

authentication.add_url_rule('/api/login' , view_func = login, methods = ['POST' , 'GET'])


@cross_origin (support_credentials=True)
@login_required
def logout():
    user_id = session.pop('user_id', None)
    session.pop ('role', None)
    logout_user()

    user = User.query.get(user_id)
    output = {'user':user.serialize_one(), 'status':'OK'}
    return jsonify (output)

authentication.add_url_rule('/api/logout' , view_func = logout)

@cross_origin (support_credentials=True)
@login_required
def change_password ():
    if request.method == 'POST':

        req = request.get_json(force = True)
        user = User.query.get (session['user_id'])
        new_pw = req['password']
        user.change_password (new_pw)

        output = {'user':user.serialize_one(), 'status':'OK'}
        return jsonify (output)

    output = {'user':user.serialize_one(), 'status':'method is not POST'}
    return jsonify (output)

authentication.add_url_rule('/api/changePassword' , view_func = change_password, methods = ['POST' , 'GET'])


@cross_origin (support_credentials=True)
@login_required
def rename ():
    if request.method == 'POST':

        req = request.get_json(force = True)
        user = User.query.get (session['user_id'])
        new_name = req['name']
        user.rename (new_name)

        output = {'user':user.serialize_one(), 'status':'OK'}
        return jsonify (output)

    output = {'user':user.serialize_one(), 'status':'method is not POST'}
    return jsonify (output)

authentication.add_url_rule('/api/rename' , view_func = rename, methods = ['POST' , 'GET'])


@cross_origin (support_credentials=True)
@login_required
def edit_motivation_count (count):
    if (int(count) < 11) and (int(count) > 0):
        user = User.query.get (session['user_id'])
        user.edit_count (int (count))

        output = {'user':user.serialize_one(), 'status':'OK'}
        return jsonify (output)

    output = {'user':user.serialize_one(), 'status':'wrong count'}
    return jsonify (output)

authentication.add_url_rule('/api/editMotivatinCount/<int:count>' , view_func = edit_motivation_count)
