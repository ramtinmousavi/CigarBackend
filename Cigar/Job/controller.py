import schedule
import time
import datetime

from Cigar.Motivation.controller import update_motivations
from Cigar.Motivation.model import UserMotivation

def motivation_updater ():
    UserMotivation.expire_yesterday()
    update_motivations()

def run_schedule ():
    schedule.every(10000).seconds.do(motivation_updater)

    while True:
        schedule.run_pending()
        time.sleep(0.5)
