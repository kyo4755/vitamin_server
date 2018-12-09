from ServerStart import app
from flask import request
from Database.database import db_session
from Database.models import UserDetail
import json


@app.route("/users/setToken", methods=['POST'])
def set_token():
    session = db_session()
    return_msg = {'result': '0000'}

    if request.method == 'POST':
        id = request.form['id']
        token = request.form['token']

        if id is None or len(id) == 0:
            return_msg['result'] = '0001'
            json_string = json.dumps(return_msg)
            return json_string

        if token is None or len(token) == 0:
            return_msg['result'] = '0002'
            json_string = json.dumps(return_msg)
            return json_string

        query = session.query(UserDetail) \
            .filter(UserDetail.id == id).first()

        if query is None:
            return_msg['result'] = '0010'
        else:
            query.token = token
            session.commit()

    else:
        return_msg['result'] = '0100'

    session.close()
    json_string = json.dumps(return_msg)
    return json_string
