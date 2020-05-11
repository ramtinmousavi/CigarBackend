from Cigar import DataBase as db

from Cigar.Authentication.model import User
from Cigar.Multimedia.model import Video, Book, Podcast
from cigar.Motivation.model import Category, SubCategory, Motivation, UserMotivation


def make_instances ():
    User ('admin','admin','admin','owner').save()
    
