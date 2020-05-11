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
