import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:rm3241365@localhost/cigardb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

DataBase = SQLAlchemy(app)
MarshMallow = Marshmallow (app)

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User_Model.query.get(user_id)

from Billboard.Authentication.model import User
from Billboard.Authentication.controller import authentication
#import all controllers

#register their blueprint
app.register_blueprint(authentication)
