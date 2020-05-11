from Cigar import DataBase as db

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import random

from Cigar import MarshMallow as ma
from flask_marshmallow import Marshmallow

from Cigar.Motivation.model import Motivation, SubCategory, UserMotivation



class User (db.Model, UserMixin):
    __tablename__ = 'user_model'

    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(50), unique=True , nullable = False)
    role = db.Column(db.String(10), nullable = False)   #user, admin, owner
    pass_hash = db.Column(db.Text)
    motivation_count = db.Column (db.Integer, nullable = False)
    usermotivations = db.relationship ('UserMotivation' , cascade = 'all,delete', backref = 'user_model' , lazy = True)



    def __init__ (self, name, email, password, role = 'user', count = 5):
        self.name = name
        self.email = email.lower()
        self.role = role
        self.pass_hash = generate_password_hash (password)
        self.motivation_count = count

    def check_password (self, password):
        return check_password_hash (self.pass_hash,password)

    def save (self):
        db.session.add (self)
        db.session.commit()

    def rename (self, new_name):
        self.name = new_name
        db.session.commit()

    def change_password (self, pw):
        self.pass_hash = generate_password_hash (pw)
        db.session.commit()

    def edit_count (self, count):
        self.motivation_count = count
        db.session.commit()

    def initialize_motivations (self):
        for subcategory in SubCategory.query.all():
            motivations = Motivation.query.filter_by (subcategory_id = subcategory.id)
            random_range = random.sample (range(motivations.count()), user.motivation_count * 7)
            for i in range (len(random_range)):
                new_record = UserMotivation (self.id, motivations[random_range[i]].id, subcategory.id, days = i%7)
                new_record.save()

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
        exclude = ('pass_hash', 'role')
