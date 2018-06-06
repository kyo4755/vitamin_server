import json

from flask import request
from Database.database import init_db, db_session
from Database.models import UserDetail

session = db_session()

if __name__ == '__main__':
    from Network import app
    from UserManage import image, login, register
    from Chatting import chat
    from Friends import friend
    init_db()
    app.run(host='0.0.0.0', debug=True)