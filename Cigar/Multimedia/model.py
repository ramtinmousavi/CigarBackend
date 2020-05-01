from Cigar import DataBase as db
from Cigar import MarshMallow as ma
from flask_marshmallow import Marshmallow

from datetime import datetime, timedelta


class Video (db.Model):
    __tablename__ = 'video_model'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column (db.String(40), nullable = False)
    description = db.Column (db.Text , nullable = False)
    url = db.Column (db.Text , nullable = False)
    timestamp = db.Column (db.DateTime)

    def __init__ (self, title, description, url):
        self.title = title
        self.description = description
        self.url = url
        self.timestamp = datetime.now()

    def save (self):
        db.session.add (self)
        db.session.commit()

    def edit (self, title, description, url):
        self.title = title
        self.description = description
        self.url = url
        db.session.commit()

    def delete (self):
        db.session.delete (self)
        db.session.commit()

    def serialize_one (self):
        return VideoSchema().dump(self)

    @staticmethod
    def serialize_many (arg):
        return VideoSchema(many=True).dump(arg)

class VideoSchema (ma.ModelSchema):
    class Meta:
        model = Video


class Book (db.Model):
    __tablename__ = 'book_model'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column (db.String(40), nullable = False)
    description = db.Column (db.Text , nullable = False)
    url = db.Column (db.Text , nullable = False)
    timestamp = db.Column (db.DateTime)

    def __init__ (self, title, description, url):
        self.title = title
        self.description = description
        self.url = url
        self.timestamp = datetime.now()

    def save (self):
        db.session.add (self)
        db.session.commit()

    def edit (self, title, description, url):
        self.title = title
        self.description = description
        self.url = url
        db.session.commit()

    def delete (self):
        db.session.delete (self)
        db.session.commit()

    def serialize_one (self):
        return BookSchema().dump(self)

    @staticmethod
    def serialize_many (arg):
        return BookSchema(many=True).dump(arg)

class BookSchema (ma.ModelSchema):
    class Meta:
        model = Book


class Podcast (db.Model):
    __tablename__ = 'podcast_model'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column (db.String(40), nullable = False)
    description = db.Column (db.Text , nullable = False)
    url = db.Column (db.Text , nullable = False)
    timestamp = db.Column (db.DateTime)

    def __init__ (self, title, description, url):
        self.title = title
        self.description = description
        self.url = url
        self.timestamp = datetime.now()

    def save (self):
        db.session.add (self)
        db.session.commit()

    def edit (self, title, description, url):
        self.title = title
        self.description = description
        self.url = url
        db.session.commit()

    def delete (self):
        db.session.delete (self)
        db.session.commit()

    def serialize_one (self):
        return PodcastSchema().dump(self)

    @staticmethod
    def serialize_many (arg):
        return PodcastSchema(many=True).dump(arg)

class PodcastSchema (ma.ModelSchema):
    class Meta:
        model = Podcast


class Motivation (db.Model):
    __tablename__ = 'motivation_model'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column (db.String(40), nullable = False)
    description = db.Column (db.Text , nullable = False)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategory_model.id'))
    timestamp = db.Column (db.DateTime)

    def __init__ (self, title, description, subcategory_id):
        self.title = title
        self.description = description
        self.timestamp = datetime.now()

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

    def edit (self, name):
        self.name = name
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


class Category (db.Model):
    __tablename__ = 'category_model'

    id = db.Column (db.Integer, primary_key = True)
    name = db.Column (db.String (30) , nullable = False, unique = True)
    subcategories = db.relationship ('SubCategory' , cascade = 'all,delete', backref = 'category_model' , lazy = True)


    def __init__ (self, name):
        self.name = name

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
