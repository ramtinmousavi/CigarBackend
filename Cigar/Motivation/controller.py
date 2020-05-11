from flask import request, jsonify, session, Blueprint
from flask_login import login_required
from flask_cors import  cross_origin

from Cigar.Motivation.model import Category, SubCategory, Motivation
from Cigar.Authentication.model import User
from Cigar import response_generator


motivation = Blueprint('motivation', __name__)


@cross_origin(supports_credentials=True)
@login_required
def get_motivations (subcategoryId):
    user = User.query.get (session['user_id'])
    motivations = user.get_to_show_motivations(subcategoryId)

    output = response_generator (Motivation.serialize_many (motivations), 200, 'OK')
    return jsonify (output)

motivation.add_url_rule('/api/getMotivations/<int:subcategoryId>' , view_func = get_motivations)


@cross_origin(supports_credentials=True)
@login_required
def get_category (categoryId = None):
    if categoryId:
        category = Category.query.get(int(categoryId))
        if (category):
            output = response_generator (category.serialize_one(), 200, 'OK')
            return jsonify (output)

        output = response_generator (None, 406, 'wrong category id')
        return jsonify (output)

    categories = Category.query.all()
    output = response_generator (Category.serialize_many (categories), 200, 'OK')
    return jsonify (output)

motivation.add_url_rule('/api/getCategory/<int:categoryId>' , view_func = get_category)
motivation.add_url_rule('/api/getCategory' , view_func = get_category)
