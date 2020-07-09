import os
from threading import Thread
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:rm3241365@localhost/cigardb'
#dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace ("\\" , '/').split(':')[1]
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+dir_path+'/DataBase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

for media in ["IMAGE", "VIDEO", "AUDIO", "DOCUMENT"]:
    key = media + "_UPLOADS"
    #app.config[key] = os.path.abspath(os.getcwd()) + "\\Cigar\\Admin\\statics\\Admin\\" + media.lower().title() + "s\\"
    app.config[key] = os.path.abspath(os.getcwd()) + "/Cigar/Admin/statics/Admin/" + media.lower().title() + "s/"

app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
app.config["ALLOWED_VIDEO_EXTENSIONS"] = ["MP4"]
app.config["ALLOWED_DOCUMENT_EXTENSIONS"] = ["PDF"]
app.config["ALLOWED_AUDIO_EXTENSIONS"] = ["MP3"]

app.config["MAX_IMAGE_FILESIZE"] = 4 * 1024 * 1024
app.config["MAX_Video_FILESIZE"] = 30 * 1024 * 1024



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


def allowed_image_filesize(filesize):
    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False

def allowed_media(media_type, filename):
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]
    key = "ALLOWED_"+media_type.upper()+"_EXTENSIONS"
    if ext.upper() in app.config[key]:
        return True
    else:
        return False

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

from Cigar.Authentication.model import User
from Cigar.Authentication.controller import authentication
from Cigar.Multimedia.controller import multimedia
from Cigar.Admin.controller import admin
from Cigar.Motivation.controller import motivation

#register their blueprint
app.register_blueprint(authentication)
app.register_blueprint(multimedia)
app.register_blueprint(admin, url_prefix = '/admin')
app.register_blueprint(motivation)
