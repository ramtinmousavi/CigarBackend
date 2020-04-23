from Cigar import DataBase as db
from Cigar import MarshMallow as ma
from flask_marshmallow import Marshmallow

from datetime import datetime, timedelta

class Category (db.Model):
    __tablename__ = 'category_model'

    id = db.Column (db.Integer, primary_key = True)
    category_name = db.Column (db.String (30) , nullable = False, unique = True)
    videos = db.relationship ('Video' , backref = 'category_model' , lazy = True)
    books = db.relationship ('model class name' , backref = 'category_model' , lazy = True)
    podcasts = db.relationship ('model class name' , backref = 'category_model' , lazy = True)
    motivations = db.relationship ('model class name' , backref = 'category_model' , lazy = True)

    def __init__ (self, name):
        self.category_name = name

    def save (self):
        db.session.add (self)
        db.session.commit()

    def serialize_one (self):
        return CategorySchema().dump(self)

    @staticmethod
    def serialize_many (arg):
        return CategorySchema(many=True).dump(arg)

class CategorySchema (ma.ModelSchema):
    class Meta:
        model = Category
