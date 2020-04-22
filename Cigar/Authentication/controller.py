from flask import request, jsonify, session, Blueprint
from flask_login import login_required, login_user, logout_user

from Cigar.Authentication.models import User

from flask_cors import  cross_origin

authentication = Blueprint('authentication', __name__)


@cross_origin(support_credentials=True)
def sign_up():
    if request.method == 'POST':
        req = request.get_json(force = True)

        name = req['name']
        email = req ['email']
        password = req ['password']

        new_user = User (name, email, password)
        new_user.save()

        output = {'user':new_user.serialize_one(), 'status':'OK'}
        return jsonify (output)

    output = {'user':'', 'status':'method is not POST'}
    return jsonify (output)

authentication.add_url_rule('/api/signup' , view_func = Authentication.sign_up, methods = ['POST' , 'GET'])


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

authentication.add_url_rule('/api/login' , view_func = Authentication.login, methods = ['POST' , 'GET'])

@cross_origin (support_credentials=True)
@login_required
def logout():
    user_id = session.pop('user_id', None)
    logout_user()

    user = User.query.get(user_id)
    output = {'user':user.serialize_one(), 'status':'OK'}
    return jsonify (output)
    
authentication.add_url_rule('/api/logout' , view_func = Authentication.logout)
