from Cigar import DataBase as db
from Cigar import MarshMallow as ma
from flask_marshmallow import Marshmallow
from marshmallow import fields

from datetime import datetime, timedelta


class Motivation (db.Model):
    __tablename__ = 'motivation_model'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column (db.String(40), nullable = True)
    description = db.Column (db.Text , nullable = False)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategory_model.id'))
    timestamp = db.Column (db.DateTime)

    def __init__ (self, description, subcategory_id, title = None):
        self.title = title
        self.description = description
        self.timestamp = datetime.now()
        if title :
            self.title = title

        SubCategory.query.get (subcategory_id).append_motivation (self)

    def save (self):
        db.session.add (self)
        db.session.commit()

    def edit (self, title, description):
        self.title = title
        self.description = description
        db.session.commit()

    def delete (self):
        db.session.delete (self)
        db.session.commit()

    def serialize_one (self):
        return MotivationSchema().dump(self)

    @staticmethod
    def serialize_many (arg):
        return MotivationSchema(many=True).dump(arg)

class MotivationSchema (ma.ModelSchema):
    class Meta:
        model = Motivation


class SubCategory (db.Model):
    __tablename__ = 'subcategory_model'

    id = db.Column (db.Integer, primary_key = True)
    name = db.Column (db.String (30) , nullable = False)
    icon_url = db.Column (db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('category_model.id'))
    motivations = db.relationship ('Motivation' , cascade = 'all,delete', backref = 'subcategory_model' , lazy = True)

    def __init__ (self, name, url, category_id):
        self.name = name
        self.icon_url = url

        Category.query.get (category_id).append_subcategory (self)

    def save (self):
        db.session.add (self)
        db.session.commit()

    def edit (self, name, icon = None):
        self.name = name
        if icon:
            self.icon_url = icon
        db.session.commit()

    def delete (self):
        db.session.delete (self)
        db.session.commit()

    def append_motivation (self, motivation):
        self.motivations.append (motivation)
        db.session.commit()

    def serialize_one (self):
        return SubCategorySchema().dump(self)

    @staticmethod
    def serialize_many (arg):
        return SubCategorySchema(many=True).dump(arg)

class SubCategorySchema (ma.ModelSchema):
    class Meta:
        model = SubCategory
    motivations = fields.Nested (MotivationSchema, many = True)


class Category (db.Model):
    __tablename__ = 'category_model'

    id = db.Column (db.Integer, primary_key = True)
    name = db.Column (db.String (30) , nullable = False, unique = True)
    #color = db.Column (db.String (10), nullable = False)
    subcategories = db.relationship ('SubCategory' , cascade = 'all,delete', backref = 'category_model' , lazy = True)


    def __init__ (self, name):#, color = '#00000000'):
        self.name = name
        #self.color = color

    def save (self):
        db.session.add (self)
        db.session.commit()

    def edit (self, name):
        self.name = name
        db.session.commit()

    def delete (self):
        db.session.delete (self)
        db.session.commit()

    def append_subcategory (self, subcategory):
        self.subcategories.append (subcategory)
        db.session.commit()

    def serialize_one (self):
        return CategorySchema().dump(self)

    @staticmethod
    def serialize_many (arg):
        return CategorySchema(many=True).dump(arg)

class CategorySchema (ma.ModelSchema):
    class Meta:
        model = Category
    subcategories = fields.Nested (SubCategorySchema, many = True)
