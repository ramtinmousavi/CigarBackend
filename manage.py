import os
from threading import Thread

from Cigar import DataBase as db
from Cigar import app
from Cigar.Job.controller import run_schedule
#from Instances import make_instances
from Cigar.Authentication.model import User #comment

from flask_script import Manager, prompt_bool

manager = Manager(app)

@manager.command
def initdb():
    db.create_all()
    User ('admin','admin','admin','owner').save()
    print ('Initialized the database')

#ask password to drop db
@manager.command
def dropdb():
    if prompt_bool(
        "Are you sure you want to lose all your data"):
        db.drop_all()
        print ('Dropped the database')


@manager.command
def run():
    app.secret_key = os.urandom(12)

    t = Thread(target = run_schedule)
    t.daemon = True
    t.start()

    app.run(debug = True, host='0.0.0.0')


if __name__ == '__main__':
    manager.run()
