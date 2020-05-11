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

def response_generator (data, stat, msg):
    output = {}
    output ['data'] = data
    output ['status'] = stat
    output ['message'] = msg
    return output

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

from Cigar.Authentication.model import User
from Cigar.Authentication.controller import authentication
from Cigar.Multimedia.controller import multimedia
from Cigar.Admin.controller import admin
from Cigar.Motivation.controller import motivation
#import all controllers

#register their blueprint
app.register_blueprint(authentication)
app.register_blueprint(multimedia)
app.register_blueprint(admin)
app.register_blueprint(motivation)
