import time
import datetime

from Cigar.Motivation.model import UserMotivation
from Cigar.Motivation.controller import update_motivations
from Cigar.Authentication.model import User

def motivation_updater ():
    UserMotivation.expire_yesterday()
    for user_id, user_count in User.query.with_entities(User.id, User.motivation_count).all():
        update_motivations(user_id,user_count)
