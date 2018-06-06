from Network import app
from flask import request
from Database.database import db_session
from Database.models import FriendsList, UserDetail

import json


@app.route('/friend_number', methods=['POST'])
def friend_number():
    session = db_session()
    return_msg = {'result': '0000', 'f_number' : ''}
    if request.method == 'POST':
        id = request.form['id']
        
        if id is None or len(id) == 0:
            return_msg['result'] = '0001'
            json_string = json.dumps(return_msg)
            return json_string
            
        query = session.query(FriendsList)\
            .filter(FriendsList.id == id).first()

        if query.friendId is None:
            num = 0
        else:
            num = len(query.friendId.split(','))
        
        return_msg['f_number'] = num
    else:
        return_msg['result'] = '0100'
        
    session.close()
    json_string = json.dumps(return_msg)
    return json_string
        

@app.route('/add_friend', methods=['POST'])
def add_friend():
    session = db_session()
    return_msg = {'result': '0000'}
    if request.method == 'POST':
        myid = request.form['myid']
        anid = request.form['anid']

        if myid is None or len(myid) == 0:
            return_msg['result'] = '0001'
            json_string = json.dumps(return_msg)
            return json_string

        if anid is None or len(anid) == 0:
            return_msg['result'] = '0002'
            json_string = json.dumps(return_msg)
            return json_string

        query = session.query(FriendsList)\
            .filter(FriendsList.id == myid).all()

        if query is None:
            return_msg['result'] = '0003'
        else:
            for friend in query:
                if friend.friendId is None:
                    tmp_str = anid
                else:
                    tmp_str = friend.friendId + ',' + anid
                friend.friendId = tmp_str

        session.commit()
    else:
        return_msg['result'] = '0100'

    session.close()
    json_string = json.dumps(return_msg)
    return json_string


@app.route('/friends_list', methods=['POST'])
def friend_list():
    session = db_session()
    return_msg = {'result': '0000', 'friends_list': []}

    if request.method == 'POST':
        id = request.form['id']

        if id is None or len(id) == 0:
            return_msg['result'] = '0001'
            json_string = json.dumps(return_msg)
            return json_string

        friends_query = session.query(FriendsList.friendId) \
            .filter(FriendsList.id == id) \
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
            return_msg['result'] = '0002'
    else:
        return_msg['result'] = '0100'

    session.close()
    json_string = json.dumps(return_msg)
    return json_string


@app.route('/find_friend', methods=['POST'])
def find_friend():
    session = db_session()
    return_msg = {'result': '0000', 'detail_info': {}}

    if request.method == 'POST':
        anid = request.form['anid']

        if anid is None or len(anid) == 0:
            return_msg['result'] = '0001'
            json_string = json.dumps(return_msg)
            return json_string

        query = session.query(UserDetail)\
            .filter(UserDetail.id == anid).all()

        if query is None:
            return_msg['result'] = '0002'
        else:
            for detail in query:
                detail_dict = {'id': detail.id,
                               'name': detail.name,
                               'image': detail.image}
                return_msg['detail_info'] = detail_dict

    else:
        return_msg['result'] = '0100'

    session.close()
    json_string = json.dumps(return_msg)
    return json_string


@app.route("/users/get_info", methods=['POST'])
def users_get_info():
    session = db_session()
    return_msg = {'result': '0000'}

    if request.method == 'POST':
        id = request.form['id']

        if id is None or len(id) == 0:
            return_msg['result'] = '0001'
            json_string = json.dumps(return_msg)
            return json_string

        query = session.query(UserDetail)\
            .filter(UserDetail.id == id).first()

        if query is None:
            return_msg['result'] = '0010'
        else:
            return_msg['name'] = query.name
            return_msg['image'] = query.image
    else:
        return_msg['result'] = '0100'

    session.close()
    json_string = json.dumps(return_msg)
    return json_string
