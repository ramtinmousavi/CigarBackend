from flask import request, jsonify, session, Blueprint
from flask_login import login_required
from flask_cors import  cross_origin

#import models from Admin or other packages
from Cigar.Authentication.model import User
from Cigar.Multimedia.model import Category, Book, Video, Podcast, Motivation

admin = Blueprint('admin', __name__)


class Admin_Required:
    def __init__ (self, params):
        self.params = params

    def __call__ (self, f):

        def wrapped_f (*args, **kwargs):
            if (session ['role'] == 'admin') or (session['role'] == 'owner'):
                return f(*args, **kwargs)
            else:
                out = {}
                for param in self.params :
                    out [param] = ''
                out ['status'] = 'access denied'

                return jsonify (out)
        wrapped_f.__name__ = f.__name__
        return wrapped_f


@cross_origin(supports_credentials=True)
@login_required
def register_admin ():
    if session['role'] == 'owner':
        if request.method == 'POST':
            req = request.get_json(force = True)

            name = req['name']
            email = req ['email']
            password = req ['password']

            if (User.query_by_email (email) is not None):
                output = {'user':'', 'status':'user already exists'}
                return jsonify (output)

            new_user = User (name, email, password, role = 'admin')
            new_user.save()

            output = {'user':new_user.serialize_one(), 'status':'OK'}
            return jsonify (output)


        output = {'user':'', 'status':'method is not POST'}
        return jsonify (output)

    output = {'user':'', 'status':'access denied'}
    return jsonify (output)

#-----------------------------------------------------------------#
#Motivation APIs

@cross_origin(supports_credentials=True)
@login_required
@Admin_Required (['motivation'])
def add_motivation (subcategoryId):
    if request.method == 'POST':
        req = request.get_json(force = True)

        if (SubCategory.query.get (int(subcategoryId))):
            title = req['title']
            description = req['description']
            new_motivation = Motivation (title, description, int(subcategoryId))
            new_motivation.save()

            output = {'motivation':new_motivation.serialize_one(), 'status':'OK'}
            return jsonify (output)

        output = {'motivation':'', 'status':'wrong subcategory id'}
        return jsonify(output)

    output = {'motivation':'', 'status':'method is not POST'}
    return jsonify (output)

admin.add_url_rule('/api/addMotivation/<int:categoryId>' , view_func = add_motivation, methods = ['POST' , 'GET'])


@cross_origin(supports_credentials=True)
@login_required
@Admin_Required (['motivation'])
def edit_motivation (motivationId):
    if request.method == 'POST':
        req = request.get_json(force = True)

        current_motivation = Motivation.query.get (int(motivationId))
        if (current_motivation is not None):

            title = req['title']
            description = req['description']
            current_motivation.edit (title, description)

            output = {'motivation':current_motivation.serialize_one(), 'status':'OK'}
            return jsonify (output)

        output = {'motivation':'', 'status':'motivation id is wrong'}
        return jsonify (output)

    output = {'motivation':'', 'status':'method is not POST'}
    return jsonify (output)

admin.add_url_rule('/api/editMotivation/<int:motivationId>' , view_func = edit_motivation, methods = ['POST' , 'GET'])


@cross_origin(supports_credentials=True)
@login_required
@Admin_Required ([])
def delete_motivation (motivationId):

    current_motivation = Motivation.query.get (int(motivationId))
    if (current_motivation is not None):
        current_motivation.delete()
        output = {'status':'OK'}
        return jsonify (output)

    output = {'status':'motivation id is wrong'}
    return jsonify (output)

admin.add_url_rule('/api/deleteMotivation/<int:motivationId>' , view_func = delete_motivation)


@cross_origin(supports_credentials=True)
@login_required
@Admin_Required (['motivation'])
def get_motivation (motivationId):

    current_motivation = Motivation.query.get (int(motivationId))
    if (current_motivation is not None):

        output = {'motivation':current_motivation.serialize_one(), 'status':'OK'}
        return jsonify (output)

    output = {'motivation':'', 'status':'motivation id is wrong'}
    return jsonify (output)


admin.add_url_rule('/api/getMotivation/<int:motivationId>' , view_func = get_motivation)


@cross_origin(supports_credentials=True)
@login_required
@Admin_Required (['motivations'])
def get_all_motivations ():

    motivations = Motivation.query.all()

    output = {'motivations': Motivation.serialize_many(motivations), 'status':'OK'}
    return jsonify(output)

admin.add_url_rule('/api/getAllMotivations/' , view_func = get_all_motivations)


@cross_origin(supports_credentials=True)
@login_required
@Admin_Required (['motivations'])
def get_all_motivations_by_category(categoryId):
    if (Category.query.get(int(categoryId))):
        subcategories = SubCategory.query.filter_by (category_id = int(categoryId))
        motivations = Motivation.query.filter (Motivation.subcategory_id.in_ (subcategories))

        output = {'motivations':Motivation.serialize_many(motivations), 'status':'OK'}
        return jsonify (output)

    output = {'motivations':'', 'status':'wrong category id'}
    return jsonify (output)

admin.add_url_rule('/api/getAllMotivationsByCategory/' , view_func = get_all_motivations_by_category)


@cross_origin(supports_credentials=True)
@login_required
@Admin_Required (['motivations'])
def get_all_motivations_by_subcategory(subcategoryId):
    if (SubCategory.query.get(int(subcategoryId))):
        motivations = Motivation.query.filter_by (subcategory_id = int(subcategoryId))

        output = {'motivations':Motivation.serialize_many(motivations), 'status':'OK'}

    output = {'motivations':'', 'status':'wrong subcategory id'}
    return jsonify (output)

admin.add_url_rule('/api/getAllMotivationsBySubcategory/' , view_func = get_all_motivations_by_subcategory)

#------------------------------------------------------#
#Video APIs

@cross_origin(supports_credentials=True)
@login_required
@Admin_Required (['video'])
def add_video ():
    if request.method == 'POST':
        req = request.get_json(force = True)

        title = req['title']
        description = req['description']
        url = req['url']

        new_video = Video (title, description, url)
        new_video.save()

        output = {'video':new_video.serialize_one(), 'status':'OK'}
        return jsonify (output)

    output = {'motivation':'', 'status':'method is not POST'}
    return jsonify (output)

admin.add_url_rule('/api/addVideo' , view_func = add_video, methods = ['POST' , 'GET'])


@cross_origin(supports_credentials=True)
@login_required
@Admin_Required (['video'])
def edit_video (videoId):
    if request.method == 'POST':
        req = request.get_json(force = True)

        current_video = Video.query.get (int(videoId))
        if (current_video is not None):

            title = req['title']
            description = req['description']
            url = req ['url']
            current_video.edit (title, description, url)

            output = {'video':current_video.serialize_one(), 'status':'OK'}
            return jsonify (output)

        output = {'video':'', 'status':'video id is wrong'}
        return jsonify (output)

    output = {'video':'', 'status':'method is not POST'}
    return jsonify (output)

admin.add_url_rule('/api/editVideo/<int:videoId>' , view_func = edit_video, methods = ['POST' , 'GET'])


@cross_origin(supports_credentials=True)
@login_required
@Admin_Required ([])
def delete_video (videoId):

    current_video = Video.query.get (int(videoId))
    if (current_video is not None):
        current_video.delete()
        output = {'status':'OK'}
        return jsonify (output)

    output = {'status':'video id is wrong'}
    return jsonify (output)

admin.add_url_rule('/api/deleteVideo/<int:videoId>' , view_func = delete_video)


@cross_origin(supports_credentials=True)
@login_required
@Admin_Required (['video'])
def get_video (videoId):

    current_video = Video.query.get (int(videoId))
    if (current_video is not None):

        output = {'video':current_video.serialize_one(), 'status':'OK'}
        return jsonify (output)

    output = {'video':'', 'status':'video id is wrong'}
    return jsonify (output)


admin.add_url_rule('/api/getVideo/<int:videoId>' , view_func = get_video)


@cross_origin(supports_credentials=True)
@login_required
@Admin_Required (['videos'])
def get_all_videos ():

    videos = Video.query.all()

    output = {'videos': Video.serialize_many(videos), 'status':'OK'}
    return jsonify(output)

admin.add_url_rule('/api/getAllVideos/' , view_func = get_all_videos)

#------------------------------------------------------#
#Book APIs

@cross_origin(supports_credentials=True)
@login_required
@Admin_Required (['book'])
def add_book ():
    if request.method == 'POST':
        req = request.get_json(force = True)

        title = req['title']
        description = req['description']
        url = req['url']

        new_book = Book (title, description, url)
        new_book.save()

        output = {'book':new_book.serialize_one(), 'status':'OK'}
        return jsonify (output)

    output = {'book':'', 'status':'method is not POST'}
    return jsonify (output)

admin.add_url_rule('/api/addBook' , view_func = add_book, methods = ['POST' , 'GET'])


@cross_origin(supports_credentials=True)
@login_required
@Admin_Required (['book'])
def edit_book (bookId):
    if request.method == 'POST':
        req = request.get_json(force = True)

        current_book = Book.query.get (int(bookId))
        if (current_book is not None):

            title = req['title']
            description = req['description']
            url = req ['url']
            current_book.edit (title, description, url)

            output = {'book':current_book.serialize_one(), 'status':'OK'}
            return jsonify (output)

        output = {'book':'', 'status':'book id is wrong'}
        return jsonify (output)

    output = {'book':'', 'status':'method is not POST'}
    return jsonify (output)

admin.add_url_rule('/api/editBook/<int:bookId>' , view_func = edit_book, methods = ['POST' , 'GET'])


@cross_origin(supports_credentials=True)
@login_required
@Admin_Required ([])
def delete_book (bookId):

    current_book = Book.query.get (int(bookId))
    if (current_book is not None):
        current_book.delete()
        output = {'status':'OK'}
        return jsonify (output)

    output = {'status':'book id is wrong'}
    return jsonify (output)

admin.add_url_rule('/api/deleteBook/<int:bookId>' , view_func = delete_book)


@cross_origin(supports_credentials=True)
@login_required
@Admin_Required (['book'])
def get_book (bookId):

    current_book = Book.query.get (int(bookId))
    if (current_book is not None):

        output = {'book':current_book.serialize_one(), 'status':'OK'}
        return jsonify (output)

    output = {'book':'', 'status':'book id is wrong'}
    return jsonify (output)


admin.add_url_rule('/api/getBook/<int:bookId>' , view_func = get_book)


@cross_origin(supports_credentials=True)
@login_required
@Admin_Required (['books'])
def get_all_books ():

    books = Book.query.all()

    output = {'books': Book.serialize_many(books), 'status':'OK'}
    return jsonify (output)

admin.add_url_rule('/api/getAllBooks/' , view_func = get_all_books)

#------------------------------------------------------#
#Podcast APIs

@cross_origin(supports_credentials=True)
@login_required
@Admin_Required (['podcast'])
def add_podcast ():
    if request.method == 'POST':
        req = request.get_json(force = True)

        title = req['title']
        description = req['description']
        url = req['url']

        new_podcast = Podcast (title, description, url)
        new_podcast.save()

        output = {'podcast':new_podcast.serialize_one(), 'status':'OK'}
        return jsonify (output)

    output = {'podcast':'', 'status':'method is not POST'}
    return jsonify (output)

admin.add_url_rule('/api/addPodcast' , view_func = add_podcast, methods = ['POST' , 'GET'])


@cross_origin(supports_credentials=True)
@login_required
@Admin_Required (['podcast'])
def edit_podcast (podcastId):
    if request.method == 'POST':
        req = request.get_json(force = True)

        current_podcast = Podcast.query.get (int(podcastId))
        if (current_podcast is not None):

            title = req['title']
            description = req['description']
            url = req ['url']
            current_podcast.edit (title, description, url)

            output = {'podcast':current_podcast.serialize_one(), 'status':'OK'}
            return jsonify (output)

        output = {'podcast':'', 'status':'podcast id is wrong'}
        return jsonify (output)

    output = {'podcast':'', 'status':'method is not POST'}
    return jsonify (output)

admin.add_url_rule('/api/editPodcast/<int:podcastId>' , view_func = edit_podcast, methods = ['POST' , 'GET'])


@cross_origin(supports_credentials=True)
@login_required
@Admin_Required ([])
def delete_podcast (podcastId):

    current_podcast = Podcast.query.get (int(podcastId))
    if (current_podcast is not None):
        current_podcast.delete()
        output = {'status':'OK'}
        return jsonify (output)

    output = {'status':'podcast id is wrong'}
    return jsonify (output)

admin.add_url_rule('/api/deletePodcast/<int:podcastId>' , view_func = delete_podcast)


@cross_origin(supports_credentials=True)
@login_required
@Admin_Required (['podcast'])
def get_podcast (podcastId):

    current_podcast = Podcast.query.get (int(podcastId))
    if (current_podcast is not None):

        output = {'podcast':current_podcast.serialize_one(), 'status':'OK'}
        return jsonify (output)

    output = {'podcast':'', 'status':'podcast id is wrong'}
    return jsonify (output)


admin.add_url_rule('/api/getPodcast/<int:podcastId>' , view_func = get_podcast)


@cross_origin(supports_credentials=True)
@login_required
@Admin_Required (['podcasts'])
def get_all_podcasts ():

    podcasts = Podcast.query.all()

    output = {'podcasts': Podcast.serialize_many(podcasts), 'status':'OK'}
    return jsonify (output)

admin.add_url_rule('/api/getAllPodcasts/' , view_func = get_all_podcasts)

#------------------------------------------------------#
#Category APIs

@cross_origin(supports_credentials=True)
@login_required
@Admin_Required (['category'])
def add_category ():
    if request.method == 'POST':
        req = request.get_json(force = True)

        name = req['name']

        new_category = Category (name)
        new_category.save()

        output = {'category':new_category.serialize_one(), 'status':'OK'}
        return jsonify (output)

    output = {'category':'', 'status':'method is not POST'}
    return jsonify (output)

admin.add_url_rule('/api/addCategory' , view_func = add_category, methods = ['POST' , 'GET'])


@cross_origin(supports_credentials=True)
@login_required
@Admin_Required (['category'])
def edit_category (categoryId):
    if request.method == 'POST':
        req = request.get_json(force = True)

        current_category = Category.query.get (int(categoryId))
        if (current_category is not None):

            name = req['name']
            current_category.edit (name)

            output = {'category':current_category.serialize_one(), 'status':'OK'}
            return jsonify (output)

        output = {'category':'', 'status':'category id is wrong'}
        return jsonify (output)

    output = {'category':'', 'status':'method is not POST'}
    return jsonify (output)

admin.add_url_rule('/api/editCategory/<int:categoryId>' , view_func = edit_category, methods = ['POST' , 'GET'])


@cross_origin(supports_credentials=True)
@login_required
@Admin_Required ([])
def delete_category (categoryId):

    current_category = Category.query.get (int(categoryId))
    if (current_category is not None):
        current_category.delete()
        output = {'status':'OK'}
        return jsonify (output)

    output = {'status':'category id is wrong'}
    return jsonify (output)

admin.add_url_rule('/api/deleteCategory/<int:categoryId>' , view_func = delete_category)

#get category , get all category
