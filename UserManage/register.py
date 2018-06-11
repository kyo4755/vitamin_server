from ServerStart import app
from flask import request
from Database.database import db_session
from Database.models import UserDetail, FriendsList
import json


@app.route("/users/idCheck", methods=['POST'])
def id_check():
    session = db_session()
    return_msg = {'result': '0000'}

    if request.method == 'POST':
        id = request.form['id']

        if id is None or len(id) == 0:
            return_msg['result'] = '0001'
            json_string = json.dumps(return_msg)
            return json_string

        query = session.query(UserDetail.id).filter(UserDetail.id == id).first()

        if query is not None:
            return_msg['result'] = '0002'

    else:
        return_msg['result'] = '0100'

    session.close()
    json_string = json.dumps(return_msg)
    return json_string


@app.route("/users/register", methods=['POST'])
def register():
    session = db_session()
    return_msg = {'result': '0000'}
    is_add_to_db = True

    if request.method == 'POST':
        id = request.form['id']
        if id is None or len(id) == 0:
            return_msg['result'] = '0001'
            is_add_to_db = False

        passwd = request.form['passwd']
        if passwd is None or len(passwd) == 0:
            return_msg['result'] = '0002'
            is_add_to_db = False

        phone_number = request.form['phone_number']
        if phone_number is None or len(phone_number) == 0:
            return_msg['result'] = '0003'
            is_add_to_db = False

        name = request.form['name']
        if name is None or len(name) == 0:
            return_msg['result'] = '0004'
            is_add_to_db = False

        email = request.form['email']
        if email is None or len(email) == 0:
            return_msg['result'] = '0005'
            is_add_to_db = False

        nation = request.form['nation']
        if nation is None or len(nation) == 0:
            return_msg['result'] = '0006'
            is_add_to_db = False

        location = request.form['location']
        if location is None or len(location) == 0:
            return_msg['result'] = '0007'
            is_add_to_db = False

        prefer_language = request.form['prefer_language']
        if prefer_language is None or len(prefer_language) == 0:
            return_msg['result'] = '0008'
            is_add_to_db = False

        if is_add_to_db:
            t = UserDetail(id, passwd, phone_number, name, email, nation, location, prefer_language)
            session.add(t)

            f = FriendsList(id)
            session.add(f)
    else:
        return_msg['result'] = '0100'

    session.commit()
    session.close()
    json_string = json.dumps(return_msg)
    return json_string
