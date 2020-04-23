from Cigar import DataBase as db

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from Cigar import MarshMallow as ma
from flask_marshmallow import Marshmallow

from Cigar.Multimedia.model import Motivation

from sqlalchemy.orm import validates
import re


#many to many relationship between users and motivations
user_motivation_table = db.Table ('user_motivation_table',
db.Column('user_id', db.Integer, db.ForeignKey('motivation_model.id')),
db.Column('motivation_id', db.Integer, db.ForeignKey('user_model.id'))
)


class User (db.Model, UserMixin):
    __tablename__ = 'user_model'

    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(50), unique=True , nullable = False)
    pass_hash = db.Column(db.Text)
    viewed_motivations = db.relationship("Motivation", secondary = user_motivation_table)


    @validates ('email')
    def validate_email (self, key, value):
        assert (re.search ('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$', value))
        return value

    def __init__ (self, name, email, password):
        self.name = name
        self.email = email.lower()
        self.pass_hash = generate_password_hash (password)

    def check_password (self, password):
        return check_password_hash (self.pass_hash,password)

    def save (self):
        db.session.add (self)
        db.session.commit()

    def append_viewed_motivation (self, motivation):
        self.viewed_motivations.append (motivation)
        db.session.commit()

    @staticmethod
    def query_by_email (email):
        return User.query.filter_by (email = email).first()

    def serialize_one (self):
        return UserSchema().dump(self)

    @staticmethod
    def serialize_many (arg):
        return UserSchema(many=True).dump(arg)

class UserSchema (ma.ModelSchema):
    class Meta:
        model = User
        exclude = ('pass_hash',)
