from flask import request, jsonify, session, Blueprint
from flask_login import login_required
from flask_cors import  cross_origin

#import models from Admin or other packages
from Cigar.Authentication.model import User

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
