from Cigar import DataBase as db

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import random

from Cigar import MarshMallow as ma
from flask_marshmallow import Marshmallow

from Cigar.Multimedia.model import Motivation


#many to many relationship between users and visited motivations
user_visited_motivation_table = db.Table ('user_visited_motivation_table',
db.Column('user_id', db.Integer, db.ForeignKey('user_model.id')),
db.Column('motivation_id', db.Integer, db.ForeignKey('motivation_model.id'))
)

#many to many relationship between users and reserve motivations
user_reserve_motivation_table = db.Table ('user_reserve_motivation_table',
db.Column('user_id', db.Integer, db.ForeignKey('user_model.id')),
db.Column('motivation_id', db.Integer, db.ForeignKey('motivation_model.id'))
)

#many to many relationship between users and current motivations
user_to_show_motivation_table = db.Table ('user_to_show_motivation_table',
db.Column('user_id', db.Integer, db.ForeignKey('user_model.id')),
db.Column('motivation_id', db.Integer, db.ForeignKey('motivation_model.id'))
)


class User (db.Model, UserMixin):
    __tablename__ = 'user_model'

    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(50), unique=True , nullable = False)
    role = db.Column(db.String(10), nullable = False)   #user, admin, owner
    pass_hash = db.Column(db.Text)
    visited_motivations = db.relationship("Motivation", secondary = user_visited_motivation_table)
    reserve_motivations = db.relationship("Motivation", secondary = user_reserve_motivation_table)
    to_show_motivations = db.relationship("Motivation", secondary = user_to_show_motivation_table)


    def __init__ (self, name, email, password, role = 'user'):
        self.name = name
        self.email = email.lower()
        self.role = role
        self.pass_hash = generate_password_hash (password)

    def check_password (self, password):
        return check_password_hash (self.pass_hash,password)

    def save (self):
        db.session.add (self)
        db.session.commit()

    def append_viewed_motivations (self, motivation):
        self.visited_motivations.extend (motivation)
        db.session.commit()

    def append_reserve_motivations (self, motivation):
        self.reserve_motivations.append (motivation)
        db.session.commit()

    def remove_reserve_motivations(self):
        self.reserve_motivations = []
        db.session.commit()

    def get_to_show_motivations (self, count = None):
        return (self.to_show_motivations)

    @staticmethod
    def update_reserve_motivations ():
        for user in User.query.all():
            all_motivations = Motivation.query.filter(~Motivation.id.in_ ([i.id for i in user.visited_motivations]))
            try:
                random_range = random.sample (range(all_motivations.count()), 10)
                user.remove_reserve_motivations()
                selected_motivations = []
                for idx in random_range:
                    user.append_reserve_motivations (all_motivations[idx])
            except ValueError:
                pass

    @staticmethod
    def update_to_show_motivations ():
        for user in User.query.all():
            user.append_viewed_motivations (user.to_show_motivations)
            user.to_show_motivations = user.reserve_motivations
        db.session.commit()
            #commit for each user or commit all ???!!!



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
        exclude = ('pass_hash', 'visited_motivations', 'reserve_motivations', 'to_show_motivations')
