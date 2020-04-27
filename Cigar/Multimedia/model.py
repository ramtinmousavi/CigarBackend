from Cigar import DataBase as db
from Cigar import MarshMallow as ma
from flask_marshmallow import Marshmallow

from datetime import datetime, timedelta

class Category (db.Model):
    __tablename__ = 'category_model'

    id = db.Column (db.Integer, primary_key = True)
    category_name = db.Column (db.String (30) , nullable = False, unique = True)
    videos = db.relationship ('Video' , backref = 'category_model' , lazy = True)
    books = db.relationship ('Book' , backref = 'category_model' , lazy = True)
    podcasts = db.relationship ('Podcast' , backref = 'category_model' , lazy = True)
    motivations = db.relationship ('model class name' , backref = 'category_model' , lazy = True)

    def __init__ (self, name):
        self.category_name = name

    def save (self):
        db.session.add (self)
        db.session.commit()

    def append_media (self, media, media_type):
        if media_type == 'video':
            self.videos.append (media)
            db.session.commit()
        elif media_type == 'book':
            self.books.append (media)
            db.session.commit()
        elif media_type == 'podcast':
            self.podcasts.append (media)
            db.session.commit()
        elif media_type == 'motivation':
            self.motivations.append (media)
            db.session.commit()

    def serialize_one (self):
        return CategorySchema().dump(self)

    @staticmethod
    def serialize_many (arg):
        return CategorySchema(many=True).dump(arg)

class CategorySchema (ma.ModelSchema):
    class Meta:
        model = Category


class Video (db.Model):
    __tablename__ = 'video_model'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column (db.String(40), nullable = False)
    description = db.Column (db.Text , nullable = False)
    url = db.Column (db.Text , nullable = False)
    category_id = db.Column(db.Integer, db.ForeignKey('category_model.id'))
    timestamp = db.Column (db.DateTime)

    def __init__ (self, title, description, url, category_id):
        self.title = title
        self.description = description
        self.url = url
        self.timestamp = datetime.now()

        Category.query.get (category_id).append_media (self, 'video')

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
    category_id = db.Column(db.Integer, db.ForeignKey('category_model.id'))
    timestamp = db.Column (db.DateTime)

    def __init__ (self, title, description, url, category_id):
        self.title = title
        self.description = description
        self.url = url
        self.timestamp = datetime.now()

        Category.query.get (category_id).append_media (self, 'book')

    def save (self):
        db.session.add (self)
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
    category_id = db.Column(db.Integer, db.ForeignKey('category_model.id'))
    timestamp = db.Column (db.DateTime)

    def __init__ (self, title, description, url, category_id):
        self.title = title
        self.description = description
        self.url = url
        self.timestamp = datetime.now()

        Category.query.get (category_id).append_media (self, 'podcast')

    def save (self):
        db.session.add (self)
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
    category_id = db.Column(db.Integer, db.ForeignKey('category_model.id'))
    timestamp = db.Column (db.DateTime)

    def __init__ (self, title, description, category_id):
        self.title = title
        self.description = description
        self.timestamp = datetime.now()

        Category.query.get (category_id).append_media (self, 'motivation')

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
