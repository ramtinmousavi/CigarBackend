from flask import request, jsonify, session, Blueprint
from flask_login import login_required
from flask_cors import  cross_origin

#import models from Admin or other packages
from Cigar.Authentication.model import User

admin = Blueprint('admin', __name__)
