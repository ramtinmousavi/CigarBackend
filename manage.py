import os

from Cigar import DataBase as db
from Cigar import app
#from Instances import make_instances

from flask_script import Manager, prompt_bool

manager = Manager(app)

@manager.command
def initdb():
    db.create_all()
    #make_instances()
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
    app.run(debug = True)


if __name__ == '__main__':
    manager.run()
