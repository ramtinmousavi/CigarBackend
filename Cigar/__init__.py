import os
from threading import Thread
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:rm3241365@localhost/cigardb'
dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace ("\\" , '/').split(':')[1]
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+dir_path+'/DataBase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

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

from Cigar.Job.controller import motivation_updater
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
scheduler = BackgroundScheduler()
scheduler.add_job(func=motivation_updater, trigger="cron", day = '*', hour = '0', minute = '1')
scheduler.start()
atexit.register(lambda: scheduler.shutdown())
