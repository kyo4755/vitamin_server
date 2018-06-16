from ServerStart import app
from flask import request
from Database.database import db_session
from Database.models import UserDetail, FriendsList
import json


@app.route("/users/login", methods=['POST'])
def login():
    session = db_session()
    return_msg = {'result': '0000', 'friends_list': [], "my_profile": {}}

    if request.method == 'POST':
        id = request.form['id']
        pw = request.form['passwd']

        if id is None or len(id) == 0:
            return_msg['result'] = '0001'
            json_string = json.dumps(return_msg)
            return json_string

        if pw is None or len(pw) == 0:
            return_msg['result'] = '0002'
            json_string = json.dumps(return_msg)
            return json_string

        query = session.query(UserDetail) \
            .filter(UserDetail.id == id, UserDetail.passwd == pw) \
            .first()

        if query is None:
            return_msg['result'] = '0003'
        else:
            my_profile = {'id': query.id,
                          'name': query.name,
                          'phone_number': query.phone_number,
                          'email': query.email,
                          'nation': query.nation,
                          'location': query.location,
                          'prefer_language': query.prefer_language,
                          'status_msg': query.status_msg,
                          'image': query.image}
            return_msg['my_profile'] = my_profile
    else:
        return_msg['result'] = '0100'

    session.close()
    json_string = json.dumps(return_msg)
    return json_string
