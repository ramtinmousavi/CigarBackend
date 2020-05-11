from Cigar import DataBase as db

from Cigar.Authentication.model import User
from Cigar.Multimedia.model import Video, Book, Podcast
from Cigar.Motivation.model import Category, SubCategory, Motivation, UserMotivation


def make_instances ():
    User ('admin','admin','admin','owner').save()

    for i in range (1,101):
        Video (str('Video'+str(i)), str('Description For Video '+ str(i)), 'google.com').save()
        Book (str('Book'+str(i)), str('Description For Book '+ str(i)), 'google.com').save()
        Podcast (str('Podcast'+str(i)), str('Description For Podcast '+ str(i)), 'google.com').save()

    for i in range (1,6):
        Category (str('Category #'+ str(i))).save()
        for j in range (1,11):
            SubCategory (str('Subcategory #'+str(j)+' From Category #'+str(i)), 'google.com', i).save()

    for x in range (1,51):
        for y in range (1,101):
            Motivation(str('Motivation #'+str(y)+ 'For SubCategory #'+str(x)),x).save()
