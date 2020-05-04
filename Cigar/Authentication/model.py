from Cigar import DataBase as db

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import random

from Cigar import MarshMallow as ma
from flask_marshmallow import Marshmallow

from Cigar.Multimedia.model import Motivation, SubCategory


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
    motivation_count = db.Column (db.Integer, nullable = False)
    visited_motivations = db.relationship("Motivation", secondary = user_visited_motivation_table)
    reserve_motivations = db.relationship("Motivation", secondary = user_reserve_motivation_table)
    to_show_motivations = db.relationship("Motivation", secondary = user_to_show_motivation_table)


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

    @staticmethod
    def query_by_email (email):
        return User.query.filter_by (email = email).first()

    def append_viewed_motivations (self, motivation):
        self.visited_motivations.extend (motivation)
        db.session.commit()

    def append_reserve_motivations (self, motivation):
        self.reserve_motivations.append (motivation)
        db.session.commit()

    def remove_reserve_motivations(self):
        self.reserve_motivations = []
        db.session.commit()

    def feed_reserve_from_visited (self, subcategory_id):
        visited_from_this_category = []
        for visited in self.visited_motivations:
            if visited.subcategory_id == subcategory_id:
                visited_from_this_category.append (visited)
        random_range = random.sample (range(len(visited_from_this_category)), self.motivation_count)
        for idx in random_range:
            self.append_reserve_motivations (visited_from_this_category[idx])
        db.session.commit()

    def get_to_show_motivations (self, subcategoryId):
        to_show_motivations = []
        for motivation in self.to_show_motivations:
            if motivation.subcategory_id == subcategoryId:
                to_show_motivations.append(motivation)
        return (to_show_motivations)

    @staticmethod
    def update_reserve_motivations ():
        all_motivations = {}
        for user in User.query.all():
            for subcategory_id, in db.session.query (SubCategory.id).all():
                all_motivations[subcategory_id] = Motivation.query.filter(~Motivation.id.in_ ([i.id for i in user.visited_motivations]),
                                                                        Motivation.subcategory_id == subcategory_id)
            user.remove_reserve_motivations()
            for i in all_motivations:   #for each subcategory
                #if  (all_motivations[i].count() ) > 5:
                try:
                    random_range = random.sample (range(all_motivations[i].count()), user.motivation_count)
                    for idx in random_range:
                        user.append_reserve_motivations (all_motivations[i][idx])
                except ValueError:
                    #if don't have enough non-visited msgs
                    #then feed reserved list randomly from old visited msgs
                    user.feed_reserve_from_visited (i) #i is current subcategory



    @staticmethod
    def update_to_show_motivations ():
        for user in User.query.all():
            user.append_viewed_motivations (user.to_show_motivations)
            user.to_show_motivations = user.reserve_motivations
        db.session.commit()
            #commit for each user or commit all ???!!!

    def serialize_one (self):
        return UserSchema().dump(self)

    @staticmethod
    def serialize_many (arg):
        return UserSchema(many=True).dump(arg)

class UserSchema (ma.ModelSchema):
    class Meta:
        model = User
        exclude = ('pass_hash', 'visited_motivations', 'reserve_motivations', 'to_show_motivations', 'role')
