from Cigar import DataBase as db

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import random

from Cigar import MarshMallow as ma
from flask_marshmallow import Marshmallow

from Cigar.Motivation.model import Motivation, SubCategory, UserMotivation


user_motivation_bookmark = db.Table ('user_motivation_bookmark',
db.Column('user_id', db.Integer, db.ForeignKey('user_model.id')),
db.Column('motivation_id', db.Integer, db.ForeignKey('motivation_model.id')))


class User (db.Model, UserMixin):
    __tablename__ = 'user_model'

    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(50), unique=True , nullable = False)
    role = db.Column(db.String(10), nullable = False)   #user, admin, owner
    pass_hash = db.Column(db.Text)
    motivation_count = db.Column (db.Integer, nullable = False)
    usermotivations = db.relationship ('UserMotivation' , cascade = 'all,delete', backref = 'user_model' , lazy = True)
    motivation_bookmark = db.relationship ('Motivation', secondary = user_motivation_bookmark)



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

    def add_bookmark (self, motivation):
        self.motivation_bookmark.append (motivation)
        db.session.commit()

    def remove_bookmark (self, motivation):
        self.motivation_bookmark.remove(motivation)
        db.session.commit()

    def get_bookmark (self):
        return self.motivation_bookmark

    def clear_visited_motivations (self):
        UserMotivation.query.filter (UserMotivation.user_id == self.id, UserMotivation.visited == False).delete()
        db.session.commit()

    @staticmethod
    def initialize_motivations (user_id, user_count):
        random.seed (user_id)
        for subcategory_id, in SubCategory.query.with_entities (SubCategory.id).all():
            motivations = Motivation.query.filter_by (subcategory_id = subcategory_id).all()
            samples = random.sample (motivations, user_count*7)
            for i in range (7):
                for j in range (user_count):
                    new_record = UserMotivation (user_id, samples[j+(i*user_count)].id, subcategory_id, days = i)
                    new_record.save()
        print ("DONE###########################################")

    @staticmethod
    def reinitialize_motivations (user_id, user_count):
        random.seed (user_id)
        for subcategory_id, in SubCategory.query.with_entities (SubCategory.id).all():
            useless_motivations = UserMotivation.query.with_entities\
                                            (UserMotivation.motivation_id)\
                                            .filter(UserMotivation.user_id == user_id,\
                                            UserMotivation.subcategory_id == subcategory_id).all()

            #motivations from this category except those which are useless
            useful_motivations = Motivation.query.filter \
                                    (~Motivation.id.in_ (useless_motivations),\
                                    Motivation.subcategory_id == subcategory_id).all()

            samples = random.sample (useful_motivations, user_count*7)
            for i in range (7):
                for j in range (user_count):
                    new_record = UserMotivation (user_id, samples[j+(i*user_count)].id, subcategory_id, days = i)
                    new_record.save()

        print ("DONE REINIT$$$$$$$$$$$##################")

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
        exclude = ('pass_hash', 'role', 'usermotivations')
