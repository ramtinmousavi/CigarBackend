import schedule
import time
import datetime

from Cigar.Motivation.model import UserMotivation
from Cigar.Motivation.controller import update_motivations


def motivation_updater ():
    UserMotivation.expire_yesterday()
    for user_id, user_count in User.query.with_entities(User.id, User.motivation_count).all():
        update_motivations(user_id,user_count)

def run_schedule ():
    schedule.every().day.at("00:01").do(motivation_updater)

    while True:
        schedule.run_pending()
        time.sleep(0.5)
