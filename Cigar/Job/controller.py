from apscheduler.schedulers.background import BackgroundScheduler
import time
import datetime
import atexit
import uwsgi

from Cigar.Motivation.model import UserMotivation
from Cigar.Motivation.controller import update_motivations
from Cigar.Authentication.model import User

def motivation_updater ():
    UserMotivation.expire_yesterday()
    for user_id, user_count in User.query.with_entities(User.id, User.motivation_count).all():
        update_motivations(user_id,user_count)

scheduler = BackgroundScheduler()
scheduler.add_job(func=motivation_updater, trigger="cron", day = '*', hour = '0', minute = '1')
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

while 1:
    sig = uwsgi.signal_wait()
    print (sig)
