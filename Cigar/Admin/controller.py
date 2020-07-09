from flask import request, jsonify, session, Blueprint
from flask import render_template, url_for, redirect, flash
from flask import current_app
from flask_login import login_required, login_user, logout_user, current_user
from flask_cors import  cross_origin
from werkzeug.utils import secure_filename
import os, re

from Cigar.Authentication.model import User
from Cigar.Multimedia.model import  Book, Video, Podcast
from Cigar.Motivation.model import Category, SubCategory, Motivation
from Cigar import response_generator,  allowed_media

admin = Blueprint('admin', __name__, template_folder = 'templates/Admin', static_folder = 'statics/Admin')


def admin_required (func):
    def wrapper (*args, **kwargs):
        if (session['role'] == 'admin') or (session['role'] == 'owner'):
            return func (*args, **kwargs)
        else:
            output = response_generator (None, 403, 'access denied')
            return jsonify (output)
    wrapper.__name__ = func.__name__
    return wrapper


def owner_required (func):
    def wrapper (*args, **kwargs):
        if (session['role'] == 'owner'):
            return func (*args, **kwargs)
        else:
            flash ('شما دسترسی لازم را ندارید')
            return redirect (url_for ('admin.admin_profile'))
    wrapper.__name__ = func.__name__
    return wrapper


def home ():
    if current_user.is_authenticated:
        return redirect (url_for('admin.admin_profile'))
    return render_template ('main.html')
admin.add_url_rule('/' , view_func = home)


def login_admin():
    if request.method == 'POST':

        email = request.form['email']
        password = request.form ['password']

        stored_user = User.query_by_email (email)
        if (stored_user is not None) and (stored_user.check_password(password)):
            if (stored_user.role == 'admin' or stored_user.role == 'owner'):
                login_user(stored_user)
                session ['user_id'] = stored_user.id
                session ['role'] = stored_user.role

                return redirect (url_for ('admin.admin_profile'))

    flash ('لطفا ایمیل و گذرواژه را به درستی وارد نمایید')
    return redirect (url_for ('admin.home'))
admin.add_url_rule('/login' , view_func = login_admin, methods = ['POST' , 'GET'])


@cross_origin(supports_credentials=True)
@login_required
@admin_required
def logout_admin ():
    session.pop('user_id', None)
    session.pop ('role', None)
    logout_user()

    flash ('با موفقیت خارج شدید. به امید دیدار مجدد')
    return redirect (url_for('admin.home'))
admin.add_url_rule('/logout' , view_func = logout_admin)


@cross_origin(supports_credentials=True)
@login_required
@admin_required
def admin_profile ():
    users_count = len(User.query.all())
    motivs_count = len(Motivation.query.all())
    category_count = len(Category.query.all())
    media_count = len(Video.query.all()) + len(Book.query.all()) + len(Podcast.query.all())
    return render_template ('adminDashboard.html', user = User.query.get(session['user_id']),\
     users_count = users_count, motivs_count = motivs_count,\
     category_count = category_count, media_count = media_count)

admin.add_url_rule('/home' , view_func = admin_profile)


@cross_origin(supports_credentials=True)
@login_required
@admin_required
def show_categories (page_num):
    categories = Category.query.paginate (per_page = 8, page = page_num, error_out = True)
    return (render_template ('categories.html', categories = categories))
admin.add_url_rule('/categories/<int:page_num>' , view_func = show_categories)


@cross_origin(supports_credentials=True)
@login_required
@admin_required
def delete_category ():
    if request.method == 'POST':
        pw = request.form ['password']
        categoryId = int(request.form ['category_id'])
        user = User.query.get (session['user_id'])
        if (user.check_password (pw)):
            current_category = Category.query.get (categoryId)
            if (current_category is not None):
                current_category.delete()
                flash ("دسته بندی با موفقیت حذف شد")
                return redirect (url_for('admin.show_categories', page_num = 1))

            flash ("دسته بندی اشتباه است")
            return redirect (url_for('admin.show_categories', page_num = 1))

        flash ('گذرواژه اشتباه است')
        return redirect (url_for('admin.show_categories', page_num = 1))

    return redirect (url_for('admin.show_categories', page_num = 1))
admin.add_url_rule('/deleteCategory' , view_func = delete_category, methods = ['POST' , 'GET'])


@cross_origin(supports_credentials=True)
@login_required
@admin_required
def new_category ():
    return render_template ('newCategory.html')
admin.add_url_rule('/newCategory' , view_func = new_category)


@cross_origin(supports_credentials=True)
@login_required
@admin_required
def add_category ():
    if request.method == 'POST':

        name = request.form['name']

        new_cat = Category (name)
        new_cat.save()

        flash ('دسته بندی با موفقیت اضافه شد')
        return redirect (url_for('admin.show_categories', page_num = 1))

    return redirect (url_for('admin.show_categories', page_num = 1))
admin.add_url_rule('/api/addCategory' , view_func = add_category, methods = ['POST' , 'GET'])


@cross_origin(supports_credentials=True)
@login_required
@admin_required
def update_category (categoryId):
    category = Category.query.get (categoryId)
    if category:
        return render_template ('editCategory.html', category = category)
    flash ('دسته بندی اشتباه است')
    return redirect (url_for('admin.show_categories', page_num = 1))
admin.add_url_rule('/updateCategory/<int:categoryId>' , view_func = update_category)


@cross_origin(supports_credentials=True)
@login_required
@admin_required
def edit_category ():
    if request.method == 'POST':
        categoryId = int(request.form ['category_id'])
        current_category = Category.query.get (categoryId)
        if (current_category is not None):

            name = request.form['name']
            current_category.edit (name)

            flash ('تغییر با موفقیت انجام شد')
            return redirect (url_for('admin.show_categories', page_num = 1))

        flash ('دسته بندی اشتباه است')
        return redirect (url_for('admin.show_categories', page_num = 1))

    return redirect (url_for('admin.show_categories', page_num = 1))
admin.add_url_rule('/api/editCategory' , view_func = edit_category, methods = ['POST' , 'GET'])

#---------------------------------------------------------------------------#
# Subcategory Views #

@cross_origin(supports_credentials=True)
@login_required
@admin_required
def show_subcategories (categoryId, page_num):
    category = Category.query.get(categoryId)
    if category:
        subcategories = SubCategory.query.filter_by(category_id = categoryId)\
        .paginate (per_page = 8, page = page_num, error_out = True)
        return (render_template ('subcategories.html', subcategories = subcategories, category = category))

    flash ('دسته بندی اشتباه است')
    return redirect (url_for('admin.show_categories', page_num = 1))
admin.add_url_rule('/subcategories/<int:categoryId>/<int:page_num>' , view_func = show_subcategories)


@cross_origin(supports_credentials=True)
@login_required
@admin_required
def delete_subcategory ():
    if request.method == 'POST':
        pw = request.form ['password']
        subcategoryId = int(request.form ['subcategory_id'])
        category_id = int(request.form ['category_id'])
        user = User.query.get (session['user_id'])
        if (user.check_password (pw)):
            current_subcategory = SubCategory.query.get (subcategoryId)
            if (current_subcategory is not None):
                current_subcategory.delete()
                flash ("زیر دسته بندی با موفقیت حذف شد")
                return redirect (url_for('admin.show_subcategories', categoryId = category_id, page_num = 1))

            flash ("زیر دسته بندی اشتباه است")
            return redirect (url_for('admin.show_subcategories', categoryId = category_id, page_num = 1))

        flash ('گذرواژه اشتباه است')
        return redirect (url_for('admin.show_subcategories', categoryId = category_id, page_num = 1))

    return redirect (url_for('admin.show_subcategories', categoryId = category_id, page_num = 1))
admin.add_url_rule('/deleteSubcategory' , view_func = delete_subcategory, methods = ['POST' , 'GET'])


@cross_origin(supports_credentials=True)
@login_required
@admin_required
def new_subcategory (categoryId):
    category = Category.query.get (categoryId)
    if category:
        return render_template ('newSubcategory.html', category = category)
    flash ('دسته بندی اشتباه است')
    return redirect (url_for('admin.show_categories', page_num = 1))
admin.add_url_rule('/newSubategory/<int:categoryId>' , view_func = new_subcategory)


@cross_origin(supports_credentials=True)
@login_required
@admin_required
def add_subcategory ():
    if request.method == 'POST':
        req = request.files
        categoryId = int(request.form ['category_id'])
        category = Category.query.get (categoryId)

        if category:
            if req:
                image = request.files ['image']
                if image.filename == '':
                    flash ('لطفا فایل ارسالی را انتخاب نمایید')
                    return redirect (url_for ('admin.new_subcategory', categoryId = categoryId))

                if allowed_media ('image', image.filename):
                    filename = secure_filename(image.filename)
                    saving_path = current_app.config['IMAGE_UPLOADS'] + filename
                    if (os.path.exists(saving_path)):
                        flash ('لطفا نام فایل را تغییر دهید')
                        return redirect (url_for ('admin.new_subcategory', categoryId = categoryId))
                    image.save (saving_path)
                    name = request.form['name']
                    new_subcat = SubCategory (name, filename, categoryId)
                    new_subcat.save()

                    flash ('زیر دسته بندی با موفقیت اضافه شد')
                    return redirect (url_for('admin.show_subcategories', categoryId = categoryId, page_num = 1))

                else:
                    flash ('فایل ارسالی مجاز نمی باشد')
                    return redirect (url_for ('admin.new_subcategory', categoryId = categoryId))

            flash ('لطفا فایل ارسالی را انتخاب کنید')
            return redirect (url_for ('admin.new_subcategory', categoryId = categoryId))



        flash ('دسته بندی اشتباه است')
        return redirect (url_for('admin.show_categories', page_num = 1))

    return redirect (url_for('admin.show_categories', page_num = 1))
admin.add_url_rule('/addSubcategory' , view_func = add_subcategory, methods = ['POST' , 'GET'])


@cross_origin(supports_credentials=True)
@login_required
@admin_required
def update_subcategory (categoryId, subcategoryId):
    category = Category.query.get (categoryId)
    if category:
        subcategory = SubCategory.query.get(subcategoryId)
        if subcategory:
            return render_template ('editSubcategory.html', category = category, subcategory = subcategory)

        flash ('زیر دسته بندی اشتباه هست')
        return redirect (url_for('admin.show_subcategories', categoryId = categoryId, page_num = 1))

    flash ('دسته بندی اشتباه است')
    return redirect (url_for('admin.show_categories', page_num = 1))
admin.add_url_rule('/updateCategory/<int:categoryId>/<int:subcategoryId>' , view_func = update_subcategory)


@cross_origin(supports_credentials=True)
@login_required
@admin_required
def edit_subcategory ():
    if request.method == 'POST':
        req = request.files
        categoryId = int(request.form ['category_id'])
        subcategoryId = int (request.form['subcategory_id'])
        current_category = Category.query.get (categoryId)
        current_subcategory = SubCategory.query.get (subcategoryId)
        if (current_category is not None):
            if (current_subcategory is not None):
                if req:
                    image = request.files ['image']
                    if image.filename == '':
                        flash ('لطفا فایل ارسالی را انتخاب نمایید')
                        return redirect (url_for ('admin.update_subcategory', categoryId = categoryId,\
                         subcategoryId = subcategoryId))

                    if allowed_media ('image', image.filename):
                        filename = secure_filename(image.filename)
                        saving_path = current_app.config['IMAGE_UPLOADS'] + filename
                        if (os.path.exists(saving_path)):
                            flash ('لطفا نام فایل را تغییر دهید')
                            return redirect (url_for ('admin.update_subcategory', categoryId = categoryId,\
                             subcategoryId = subcategoryId))
                        image.save (saving_path)
                        name = request.form['name']
                        current_subcategory.edit (name, filename)

                        flash ('زیر دسته بندی با موفقیت ویرایش شد')
                        return redirect (url_for('admin.show_subcategories', categoryId = categoryId, page_num = 1))

                    else:
                        flash ('فایل ارسالی مجاز نمی باشد')
                        return redirect (url_for ('admin.update_subcategory', categoryId = categoryId,\
                         subcategoryId = subcategoryId))

                flash ('لطفا فایل ارسالی را انتخاب کنید')
                return redirect (url_for ('admin.update_subcategory', categoryId = categoryId,\
                 subcategoryId = subcategoryId))

            flash ('زیر دسته بندی اشتباه است')
            return redirect (url_for('admin.show_subcategories', categoryId = categoryId, page_num = 1))

        flash ('دسته بندی اشتباه است')
        return redirect (url_for('admin.show_categories', page_num = 1))

    return redirect (url_for('admin.show_categories', page_num = 1))
admin.add_url_rule('/editSubcategory' , view_func = edit_subcategory, methods = ['POST' , 'GET'])

#------------------------------------------------------------------------------#
# Motivation Views #

@cross_origin(supports_credentials=True)
@login_required
@admin_required
def show_motivations (categoryId, subcategoryId, page_num):
    category = Category.query.get(categoryId)
    if category:
        subcategory = SubCategory.query.get (subcategoryId)
        if subcategory:
            motivations = Motivation.query.filter_by(subcategory_id = subcategoryId)\
            .paginate (per_page = 8, page = page_num, error_out = True)

            return (render_template ('motivations.html', motivations = motivations,\
             subcategory = subcategory, category = category))

        flash ('زیر دسته بندی اشتباه است')
        return redirect (url_for('admin.show_subcategories', categoryId = categoryId, page_num = 1))

    flash ('دسته بندی اشتباه است')
    return redirect (url_for('admin.show_categories', page_num = 1))
admin.add_url_rule('/motivations/<int:categoryId>/<int:subcategoryId>/<int:page_num>' , view_func = show_motivations)


@cross_origin(supports_credentials=True)
@login_required
@admin_required
def delete_motivation ():
    if request.method == 'POST':
        pw = request.form ['password']
        subcategoryId = int(request.form ['subcategory_id'])
        category_id = int(request.form ['category_id'])
        motivation_id = int (request.form ['motivation_id'])
        user = User.query.get (session['user_id'])
        if (user.check_password (pw)):
            current_motivation = Motivation.query.get (motivation_id)
            if (current_motivation is not None):
                current_motivation.delete()
                flash ("پیام با موفقیت حذف شد")
                return redirect (url_for('admin.show_motivations', categoryId = category_id,\
                 subcategoryId = subcategoryId, page_num = 1))

            flash ("لطفا پیام را به درستی انتخاب نمایید")
            return redirect (url_for('admin.show_motivations', categoryId = category_id,\
             subcategoryId = subcategoryId, page_num = 1))

        flash ('گذرواژه اشتباه است')
        return redirect (url_for('admin.show_motivations', categoryId = category_id,\
         subcategoryId = subcategoryId, page_num = 1))

    return redirect (url_for('admin.show_motivations', categoryId = category_id,\
     subcategoryId = subcategoryId, page_num = 1))
admin.add_url_rule('/deleteMotivation' , view_func = delete_motivation, methods = ['POST' , 'GET'])



@cross_origin(supports_credentials=True)
@login_required
@admin_required
def new_motivation (categoryId, subcategoryId):
    category = Category.query.get (categoryId)
    subcategory = SubCategory.query.get(subcategoryId)
    if category:
        if (subcategory and subcategory.category_id == categoryId):
            return render_template ('newMotivation.html', category = category, subcategory = subcategory)
        flash ('زیر دسته بندی اشتباه است')
        return redirect (url_for('admin.show_subcategories', categoryId = categoryId, page_num = 1))

    flash ('دسته بندی اشتباه است')
    return redirect (url_for('admin.show_categories', page_num = 1))
admin.add_url_rule('/newMotivation/<int:categoryId>/<int:subcategoryId>' , view_func = new_motivation)


@cross_origin(supports_credentials=True)
@login_required
@admin_required
def add_motivation ():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form ['description']
        subcategory_id = request.form ['subcategory_id']
        category_id = request.form ['category_id']

        new_motiv = Motivation (description, subcategory_id, title = title)
        new_motiv.save()

        flash ('پیام با موفقیت اضافه شد')
        return redirect (url_for('admin.show_motivations', categoryId = category_id,\
         subcategoryId = subcategory_id, page_num = 1))

    return redirect (url_for('admin.show_motivations', categoryId = category_id,\
     subcategoryId = subcategory_id, page_num = 1))
admin.add_url_rule('/addMotivation' , view_func = add_motivation, methods = ['POST' , 'GET'])


@cross_origin(supports_credentials=True)
@login_required
@admin_required
def update_motivation (categoryId):
    category = Category.query.get (categoryId)
    if category:
        return render_template ('editCategory.html', category = category)
    flash ('دسته بندی اشتباه است')
    return redirect (url_for('admin.show_categories', page_num = 1))
admin.add_url_rule('/updateCategory/<int:categoryId>' , view_func = update_category)

@cross_origin(supports_credentials=True)
@login_required
@admin_required
def update_motivation (categoryId, subcategoryId, motivationId):
    category = Category.query.get (categoryId)
    subcategory = SubCategory.query.get(subcategoryId)
    motivation = Motivation.query.get(motivationId)
    if category and subcategory:
        if motivation:
            return render_template ('editMotivation.html', category = category,\
            subcategory = subcategory, motivation = motivation)

        flash ('لطفا پیام را به درستی انتخاب نمایید')
        return redirect (url_for('admin.show_motivations', categoryId = categoryId,\
        subcategoryId = subcategoryId, page_num = 1))

    flash ('دسته بندی اشتباه است')
    return redirect (url_for('admin.show_categories', page_num = 1))
admin.add_url_rule('/updateMotivation/<int:categoryId>/<int:subcategoryId>/<int:motivationId>' , view_func = update_motivation)


@cross_origin(supports_credentials=True)
@login_required
@admin_required
def edit_motivation ():
    if request.method == 'POST':
        categoryId = int(request.form ['category_id'])
        subcategoryId = int (request.form['subcategory_id'])
        motivationId = int (request.form['motivation_id'])

        current_motivation = Motivation.query.get (motivationId)
        if ((current_motivation is not None) and (current_motivation.subcategory_id==subcategoryId)):

            title = request.form['title']
            description = request.form['description']
            current_motivation.edit (title, description)

            flash ('تغییر با موفقیت انجام شد')
            return redirect (url_for('admin.show_motivations',categoryId = categoryId,\
             subcategoryId = subcategoryId, page_num = 1))

        flash ('دسته بندی اشتباه است')
        return redirect (url_for('admin.show_categories', page_num = 1))

    return redirect (url_for('admin.show_categories', page_num = 1))
admin.add_url_rule('/editMotivation' , view_func = edit_motivation, methods = ['POST' , 'GET'])

#------------------------------------------------------------------------------#
# Video Views #
@cross_origin(supports_credentials=True)
@login_required
@admin_required
def show_videos (page_num):
    videos = Video.query.paginate (per_page = 8, page = page_num, error_out = True)
    return (render_template ('videos.html', videos = videos))
admin.add_url_rule('/videos/<int:page_num>' , view_func = show_videos)


@cross_origin(supports_credentials=True)
@login_required
@admin_required
def delete_video (videoId):
    video = Video.query.get (videoId)
    pw = request.form['password']
    user = User.query.get (session['user_id'])
    if video:
        if (user.check_password (pw)):
            video.delete()
            flash ('ویدیو با موفقیت حذف شد')
            return redirect (url_for('admin.show_videos', page_num = 1))

        flash ('لطفا پسورد را به درستی وارد نمایید')
        return redirect (url_for('admin.show_videos', page_num = 1))
admin.add_url_rule('/deleteVideo/<int:videoId>' , view_func = delete_video, methods = ['POST' , 'GET'])


@cross_origin(supports_credentials=True)
@login_required
@admin_required
def new_video ():
    return render_template ('newVideo.html')
admin.add_url_rule('/newVideo' , view_func = new_video)


@cross_origin(supports_credentials=True)
@login_required
@admin_required
def add_video ():
    if request.method == 'POST':
        req = request.files
        if req:
            video = request.files ['video']
            if video.filename == '':
                flash ('لطفا فایل ارسالی را انتخاب نمایید')
                return redirect (url_for ('admin.new_video'))

            if allowed_media ('video', video.filename):
                filename = secure_filename(video.filename)
                saving_path = current_app.config['VIDEO_UPLOADS'] + filename
                if (os.path.exists(saving_path)):
                    flash ('لطفا نام فایل را تغییر دهید')
                    return redirect (url_for ('admin.new_video'))
                video.save (saving_path)
                title = request.form['title']
                description = request.form['description']
                new_vid = Video (title, description, filename)
                new_vid.save()

                flash ('ویدیو با موفقیت اضافه شد')
                return redirect (url_for('admin.show_videos', page_num = 1))

            else:
                flash ('فایل ارسالی مجاز نمی باشد')
                return redirect (url_for ('admin.new_video'))

        flash ('لطفا فایل ارسالی را انتخاب کنید')
        return redirect (url_for ('admin.new_video'))

    return redirect (url_for('admin.show_videos', page_num = 1))
admin.add_url_rule('/addVideo' , view_func = add_video, methods = ['POST' , 'GET'])
#------------------------------------------------------------------------------#
# Book Views #
@cross_origin(supports_credentials=True)
@login_required
@admin_required
def show_books (page_num):
    books = Book.query.paginate (per_page = 8, page = page_num, error_out = True)
    return (render_template ('books.html', books = books))
admin.add_url_rule('/books/<int:page_num>' , view_func = show_books)


@cross_origin(supports_credentials=True)
@login_required
@admin_required
def delete_book (bookId):
    book = Book.query.get (bookId)
    pw = request.form['password']
    user = User.query.get (session['user_id'])
    if book:
        if (user.check_password (pw)):
            book.delete()
            flash ('کتاب با موفقیت حذف شد')
            return redirect (url_for('admin.show_books', page_num = 1))

        flash ('لطفا پسورد را به درستی وارد نمایید')
        return redirect (url_for('admin.show_books', page_num = 1))
admin.add_url_rule('/deleteBook/<int:bookId>' , view_func = delete_book, methods = ['POST' , 'GET'])


@cross_origin(supports_credentials=True)
@login_required
@admin_required
def new_book ():
    return render_template ('newBook.html')
admin.add_url_rule('/newBook' , view_func = new_book)


@cross_origin(supports_credentials=True)
@login_required
@admin_required
def add_book ():
    if request.method == 'POST':
        req = request.files
        if req:
            book = request.files ['book']
            if book.filename == '':
                flash ('لطفا فایل ارسالی را انتخاب نمایید')
                return redirect (url_for ('admin.new_book'))

            if allowed_media ('document', book.filename):
                filename = secure_filename(book.filename)
                saving_path = current_app.config['DOCUMENT_UPLOADS'] + filename
                if (os.path.exists(saving_path)):
                    flash ('لطفا نام فایل را تغییر دهید')
                    return redirect (url_for ('admin.new_book'))
                book.save (saving_path)
                title = request.form['title']
                description = request.form['description']
                new_bk = Book (title, description, filename)
                new_bk.save()

                flash ('کتاب با موفقیت افزوده شد')
                return redirect (url_for('admin.show_books', page_num = 1))

            else:
                flash ('فایل ارسالی مجاز نمی باشد')
                return redirect (url_for ('admin.new_book'))

        flash ('لطفا فایل ارسالی را انتخاب کنید')
        return redirect (url_for ('admin.new_book'))

    return redirect (url_for('admin.show_books', page_num = 1))
admin.add_url_rule('/addBook' , view_func = add_book, methods = ['POST' , 'GET'])

#------------------------------------------------------------------------------#
# Podcast Views #
@cross_origin(supports_credentials=True)
@login_required
@admin_required
def show_podcasts (page_num):
    podcasts = Podcast.query.paginate (per_page = 8, page = page_num, error_out = True)
    return (render_template ('podcasts.html', podcasts = podcasts))
admin.add_url_rule('/podcasts/<int:page_num>' , view_func = show_podcasts)


@cross_origin(supports_credentials=True)
@login_required
@admin_required
def delete_podcast (podcastId):
    podcast = Podcast.query.get (podcastId)
    pw = request.form['password']
    user = User.query.get (session['user_id'])
    if podcast:
        if (user.check_password (pw)):
            podcast.delete()
            flash ('پادکست با موفقیت حذف شد')
            return redirect (url_for('admin.show_podcasts', page_num = 1))

        flash ('لطفا پسورد را به درستی وارد نمایید')
        return redirect (url_for('admin.show_podcasts', page_num = 1))
admin.add_url_rule('/deletePodcast/<int:podcastId>' , view_func = delete_podcast, methods = ['POST' , 'GET'])


@cross_origin(supports_credentials=True)
@login_required
@admin_required
def new_podcast ():
    return render_template ('newPodcast.html')
admin.add_url_rule('/newPodcast' , view_func = new_podcast)


@cross_origin(supports_credentials=True)
@login_required
@admin_required
def add_podcast ():
    if request.method == 'POST':
        req = request.files
        if req:
            podcast = request.files ['podcast']
            if podcast.filename == '':
                flash ('لطفا فایل ارسالی را انتخاب نمایید')
                return redirect (url_for ('admin.new_podcast'))

            if allowed_media ('audio', podcast.filename):
                filename = secure_filename(podcast.filename)
                saving_path = current_app.config['AUDIO_UPLOADS'] + filename
                if (os.path.exists(saving_path)):
                    flash ('لطفا نام فایل را تغییر دهید')
                    return redirect (url_for ('admin.new_podcast'))
                podcast.save (saving_path)
                title = request.form['title']
                description = request.form['description']
                new_pod = Podcast (title, description, filename)
                new_pod.save()

                flash ('پادکست با موفقیت اضافه شد')
                return redirect (url_for('admin.show_podcasts', page_num = 1))

            else:
                flash ('فایل ارسالی مجاز نمی باشد')
                return redirect (url_for ('admin.new_podcast'))

        flash ('لطفا فایل ارسالی را انتخاب کنید')
        return redirect (url_for ('admin.new_podcast'))

    return redirect (url_for('admin.show_podcasts', page_num = 1))
admin.add_url_rule('/addPodcast' , view_func = add_podcast, methods = ['POST' , 'GET'])

#------------------------------------------------------------------------------#

@cross_origin(supports_credentials=True)
@login_required
@owner_required
def show_admins(page_num):
    admins = User.query.filter(User.role == 'admin').paginate (per_page = 8, page = page_num, error_out = True)
    return (render_template ('admins.html', admins = admins))
admin.add_url_rule('/admins/<int:page_num>' , view_func = show_admins)


@cross_origin(supports_credentials=True)
@login_required
@owner_required
def delete_admin(adminId):
    admin = User.query.get (adminId)
    pw = request.form['password']
    user = User.query.get (session['user_id'])
    if admin:
        if (user.check_password (pw)):
            admin.delete()
            flash ('ادمین با موفقیت حذف شد')
            return redirect (url_for('admin.show_admins', page_num = 1))

        flash ('لطفا پسورد را به درستی وارد نمایید')
        return redirect (url_for('admin.show_admins', page_num = 1))
admin.add_url_rule('/deleteAdmin/<int:adminId>' , view_func = delete_admin, methods = ['POST' , 'GET'])


@cross_origin(supports_credentials=True)
@login_required
@owner_required
def new_admin():
    return render_template ('newAdmin.html')
admin.add_url_rule('/newAdmin' , view_func = new_admin)


@cross_origin(supports_credentials=True)
@login_required
@owner_required
def add_admin ():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form ['email']
        password = request.form ['password']

        if (User.query_by_email (email) is not None):
            flash ('کاربر تکراری است')
            return redirect (url_for ('admin.add_admin'))

        if not (re.search ('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$', email)):
            flash ('ایمیل را به درستی وارد نمایید')
            return redirect (url_for ('admin.add_admin'))

        new_user = User (name, email, password, role = 'admin')
        new_user.save()

        flash ('ثبت نام با موفقیت انجام شد')
        return redirect (url_for ('admin.show_admins', page_num = 1))

    return redirect (url_for ('admin.admin_profile'))

admin.add_url_rule('/api/addAdmin' , view_func = add_admin, methods = ['POST' , 'GET'])
