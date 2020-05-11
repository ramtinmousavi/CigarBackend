import schedule
import time
import datetime

from Cigar.Motivation.controller import update_motivations
from Cigar.Motivation.model import expire_yesterday

def motivation_updater ():
    expire_yesterday()
    update_motivations()

def run_schedule ():
    schedule.every(10000).seconds.do(motivation_updater)

    while True:
        schedule.run_pending()
        time.sleep(0.5)
