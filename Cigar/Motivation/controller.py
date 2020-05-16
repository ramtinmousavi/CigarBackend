from flask import request, jsonify, session, Blueprint
from flask_login import login_required
from flask_cors import  cross_origin

from Cigar.Motivation.model import Category, SubCategory, Motivation, UserMotivation
from Cigar.Authentication.model import User
from Cigar import response_generator

from datetime import datetime, timedelta
import random


motivation = Blueprint('motivation', __name__)


@cross_origin(supports_credentials=True)
@login_required
def get_motivations (subcategoryId):
    user = User.query.get (session['user_id'])
    print (user.id, "REQ FOR MOTIV")
    motivations = []
    motivation_ids = UserMotivation.query.with_entities\
                    (UserMotivation.motivation_id)\
                    .filter (UserMotivation.user_id == user.id,\
                    UserMotivation.subcategory_id == subcategoryId,\
                    UserMotivation.timestamp == datetime.now().date())
                    #add visited == False condition !?
    for motivation_id in motivation_ids:
        motivations.append (Motivation.query.get (motivation_id))

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




def update_motivations (user_id, user_count, duration = 6):
    random.seed (user_id)
    #TODO: if data for 6 days later not in UserMotivation then
    for subcategory_id, in SubCategory.query.with_entities (SubCategory.id).all():
        #visited or reserved motivations of this users from this category
        #this variable holds useless motivation IDs
        useless_motivations = UserMotivation.query.with_entities\
                                        (UserMotivation.motivation_id)\
                                        .filter(UserMotivation.user_id == user_id,\
                                        UserMotivation.subcategory_id == subcategory_id).all()

        #motivations from this category except those which are useless
        useful_motivations = Motivation.query.filter \
                                (~Motivation.id.in_ (useless_motivations),\
                                Motivation.subcategory_id == subcategory_id).all()
        try:
            samples = random.sample (useful_motivations, user_count)
            for i in samples:
                new_record = UserMotivation (user_id, i.id, subcategory_id, duration)
                new_record.save()

        except ValueError:
            visited_motivations = UserMotivation.query.with_entities\
                                    (UserMotivation.motivation_id)\
                                    .filter(UserMotivation.user_id == user_id,\
                                    UserMotivation.subcategory_id == subcategory_id,\
                                    UserMotivation.visited == True)

            samples2 = random.sample (visited_motivations, user_count)
            for j in samples2:
                new_record = UserMotivation (user_id, j.id, subcategory_id, duration)
                new_record.save()
