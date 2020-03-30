
from views import *

def creat_app():
    from db import db
    db.create_all()

if __name__ == '__main__':
    #creat_app()
    app.run()


