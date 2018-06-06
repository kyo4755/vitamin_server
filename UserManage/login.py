from Network import app
from flask import request
from Database.database import db_session
from Database.models import UserDetail, FriendsList
import json


@app.route("/login", methods=['POST'])
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

            find_id = query.id
            friends_query = session.query(FriendsList.friendId) \
                .filter(FriendsList.id == find_id) \
                .first()

            if friends_query[0] is not None:
                friends_list = friends_query[0].split(',')

                detail_query = session.query(UserDetail) \
                    .filter(UserDetail.id.in_([friend_id for friend_id in friends_list])) \
                    .order_by(UserDetail.name) \
                    .all()
                for detail in detail_query:
                    detail_dict = {'id': detail.id,
                                   'name': detail.name,
                                   'email': detail.email,
                                   'nation': detail.nation,
                                   'location': detail.location,
                                   'prefer_language': detail.prefer_language,
                                   'status_msg': detail.status_msg,
                                   'image': detail.image}
                    return_msg['friends_list'].append(detail_dict)
            else:
                return_msg['result'] = '0004'
    else:
        return_msg['result'] = '0100'

    session.close()
    json_string = json.dumps(return_msg)
    return json_string
