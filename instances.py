from Cigar import DataBase as db

from Cigar.Authentication.model import User
from Cigar.Multimedia.model import Video, Book, Podcast
from Cigar.Motivation.model import Category, SubCategory, Motivation, UserMotivation

vid = ['1.mp4', '2.mp4']
book = ['1.pdf']
pod = ['1.mp3', '2.mp3', '3.mp3']
img = []
for i in range (1,11):
    img.append (str(i)+ '.jpg')

def make_instances ():
    db.create_all()
    User ('Admin','admin','admin3241365','owner').save()

    for i in range (1,51):
        Video (str('ویدیو '+str(i)), str('توضیحات برای ویدیو '+ str(i)), vid [i%2]).save()
        Book (str('کتاب '+str(i)), str('توضیحات برای کتاب '+ str(i)), book [0]).save()
        Podcast (str('پادکست '+str(i)), str('توضیحات برای پادکست '+ str(i)), pod [i%3]).save()

    for i in range (1,6):
        Category (str('دسته بندی شماره '+ str(i))).save()
        for j in range (1,11):
            SubCategory (str('زیردسته شماره '+str(j)+' از دسته بندی شماره '+str(i)), img [j-1], i).save()

    for x in range (1,51):
        for y in range (1,51):
            Motivation(str('پیام شماره '+str(y)+ ' از زیردسته شماره '+str(x)),x).save()

if __name__ == '__main__' :
    make_instances()
