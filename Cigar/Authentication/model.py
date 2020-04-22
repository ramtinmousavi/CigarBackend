from Cigar import DataBase as db

from flask_login import UserMixin
from werkzeug import generate_password_hash, check_password_hash

from Cigar import MarshMallow as ma
from flask_marshmallow import Marshmallow


class User (db.Model, UserMixin):
    __tablename__ = 'user_model'

    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(50), unique=True , nullable = False)
    pass_hash = db.Column(db.String(54))

    @validates ('email')
    def validate_email (self, key, value):
        #assert email bad format
        pass

    def __init__ (self, name, email, password):
        self.name = name
        self.email = email
        self.pass_hash = generate_password_hash (password)

    def save (self):
        db.session.add (self)
        db.session.commit()

    def check_password (self, password):
        return check_password_hash (self.pass_hash,password)

    def serialize_one (self):
        return UserSchema().dump(self).data

    @staticmethod
    def serialize_many (arg):
        return UserSchema(many=True).dump(arg).data

class UserSchema (ma.ModelSchema):
    class Meta:
        model = User
        exclude = ('pass_hash')
