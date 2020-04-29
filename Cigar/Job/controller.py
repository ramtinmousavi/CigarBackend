import schedule
import time
import datetime

from Cigar.Authentication.model import User

def run_schedule ():
    #schedule.every().day.at("00:00").do(User.update_to_show_motivations)
    #schedule.every().day.at("12:00").do(User.update_reserve_motivations)
    schedule.every(10).seconds.do(User.update_to_show_motivations)
    schedule.every(25).seconds.do(User.update_reserve_motivations)

    while True:
        schedule.run_pending()
        time.sleep(0.5)
