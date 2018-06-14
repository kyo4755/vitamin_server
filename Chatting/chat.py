from ServerStart import app
from flask import request
from Database.database import db_session
from Database.models import UserDetail, ChatRoom, ChatRoomDetail
import json
import requests

fcm_url = 'https://fcm.googleapis.com/fcm/send'
server_key = 'AAAAyvS5iT4:APA91bHy4GIF82ZDMNisnD2qb92aJpehF6j3xHIhDjHOE4uWjUdnfT0bfa0jbIuRKzMLRAL-82BISkMqcR99tG8RlyunZs6aGvhBb3Utr0qbJiYSQLQRon7GsXjXK3Iz0YkIcLei7aRy'
headers = {
    'Authorization': 'key= ' + server_key,
    'Content-Type': 'application/json',
}


@app.route("/chattings/getList", methods=['POST'])
def chat_list():
    session = db_session()
    return_msg = {'result': '0000', 'chat_list': []}

    if request.method == 'POST':
        id = request.form['id']
        if id is None or len(id) == 0:
            return_msg['result'] = '0001'
            json_string = json.dumps(return_msg)
            return json_string

        query = session.query(ChatRoom) \
            .filter(ChatRoom.id == id).all()

        if query is None:
            return_msg['result'] = '0002'
        else:
            for detail in query:
                query_recent = session.query(ChatRoomDetail) \
                    .filter(ChatRoomDetail.room_num == detail.room_num) \
                    .order_by(ChatRoomDetail.date.desc()).all()
                chat_detail = {}
                room_num_list = []
                for detail_recent in query_recent:
                    if room_num_list.count(detail_recent.room_num) == 0:
                        room_num_list.append(detail_recent.room_num)

                        friends_list = detail.member.split(',')
                        friends_detail = []
                        for detail_user in friends_list:
                            query_user = session.query(UserDetail) \
                                .filter(UserDetail.id == detail_user).first()

                            friends_dict = {'id': query_user.id,
                                            'name': query_user.name,
                                            'image': query_user.image}

                            friends_detail.append(friends_dict)

                        chat_detail = {'room_num': str(detail_recent.room_num),
                                       'date': str(detail_recent.date),
                                       'msg': detail_recent.msg,
                                       'friends_detail': friends_detail}

                return_msg['chat_list'].append(chat_detail)

    else:
        return_msg['result'] = '0100'

    session.close()
    json_string = json.dumps(return_msg)
    return json_string


@app.route("/chattings/send", methods=['POST'])
def chat_send():
    session = db_session()
    return_msg = {'result': '0000', 'chat_log': []}

    if request.method == 'POST':
        id = request.form['myid']
        room_num = request.form['room_num']
        msg = request.form['msg']
        date = request.form['date']

        if id is None or len(id) == 0:
            return_msg['result'] = '0001'
            json_string = json.dumps(return_msg)
            return json_string

        if room_num is None or len(room_num) == 0:
            return_msg['result'] = '0002'
            json_string = json.dumps(return_msg)
            return json_string

        if msg is None or len(msg) == 0:
            return_msg['result'] = '0003'
            json_string = json.dumps(return_msg)
            return json_string

        if date is None or len(date) == 0:
            return_msg['result'] = '0004'
            json_string = json.dumps(return_msg)
            return json_string

        t = ChatRoomDetail(room_num, id, date, msg)
        session.add(t)

        query_friend = session.query(ChatRoom.member) \
            .filter(ChatRoom.room_num == room_num).first()

        split_friend = query_friend[0].split(',')

        query_send_friend = session.query(UserDetail) \
            .filter(UserDetail.id == id).first()

        for friend in split_friend:
            if friend == id:
                continue

            message_body = {'id': id,
                            'date': date,
                            'msg': msg,
                            'name': query_send_friend.name,
                            'image': query_send_friend.image}

            print(message_body)

            query_user = session.query(UserDetail) \
                .filter(UserDetail.id == friend).first()

            data = {
                'to': query_user.token,
                'data': {
                    'message_body': message_body,
                }
            }

            response = requests.post(fcm_url, headers=headers, data=json.dumps(data))

    else:
        return_msg['result'] = '0100'

    session.commit()
    session.close()
    json_string = json.dumps(return_msg)
    return json_string


@app.route("/chattings/open", methods=['POST'])
def chat_open():
    session = db_session()
    return_msg = {'result': '0000', 'room_num': 'none'}

    if request.method == 'POST':
        my_id = request.form['myid']
        member = request.form['member']

        if my_id is None or len(my_id) == 0:
            return_msg['result'] = '0001'
            json_string = json.dumps(return_msg)
            return json_string

        if member is None or len(member) == 0:
            return_msg['result'] = '0002'
            json_string = json.dumps(return_msg)
            return json_string

        query = session.query(ChatRoom) \
            .filter(ChatRoom.id == my_id, ChatRoom.member == member).first()

        if query is None:
            query_recent_num = session.query(ChatRoomDetail) \
                .order_by(ChatRoomDetail.room_num).first()

            if query_recent_num is None:
                next_room_num = "1"
            else:
                next_room_num = str(int(query_recent_num.room_num) + 1)

            member_list = member.split(',')

            for friend in member_list:
                t = ChatRoom(friend, next_room_num, member)
                session.add(t)

            session.commit()
            return_msg['room_num'] = next_room_num

        else:
            return_msg['room_num'] = query.room_num
    else:
        return_msg['result'] = '0100'

    session.close()
    json_string = json.dumps(return_msg)
    return json_string


@app.route("/chattings/load", methods=['POST'])
def chat_load():
    session = db_session()
    return_msg = {'result': '0000', 'chat_load': []}

    if request.method == 'POST':
        room_num = request.form['room_num']
        if room_num is None or len(room_num) == 0:
            return_msg['result'] = '0001'
            json_string = json.dumps(return_msg)
            return json_string

        query = session.query(ChatRoomDetail) \
            .filter(ChatRoomDetail.room_num == room_num).order_by(ChatRoomDetail.date).all()

        for detail in query:
            query_user = session.query(UserDetail).filter(UserDetail.id == detail.id).first()
            if query_user is None:
                return_msg['result'] = '0010'
            else:
                log_dict = {'id': detail.id,
                            'date': str(detail.date),
                            'msg': detail.msg,
                            'name': query_user.name,
                            'image': query_user.image}
                return_msg['chat_load'].append(log_dict)

    else:
        return_msg['result'] = '0100'

    session.close()
    json_string = json.dumps(return_msg)
    return json_string


@app.route("/chattings/recent", methods=['POST'])
def chat_recent():
    session = db_session()
    return_msg = {'result': '0000', 'chat_recent': []}

    if request.method == 'POST':
        room_num = request.form['room_num']

        if room_num is None or len(room_num) == 0:
            return_msg['result'] = '0001'
            json_string = json.dumps(return_msg)
            return json_string

        query = session.query(ChatRoomDetail) \
            .filter(ChatRoomDetail.room_num) \
            .order_by(ChatRoomDetail.date).first()

        if query is None:
            return_msg['result'] = '0010'
        else:
            query_user = session.query(UserDetail).filter(UserDetail.id == query.id).first()
            if query_user is None:
                return_msg['result'] = '0011'
            else:
                chat_dict = {'id': query.id,
                             'date': query.date,
                             'msg': query.msg,
                             'name': query_user.name,
                             'image': query_user.image}
                return_msg['chat_recent'].append(chat_dict)
    else:
        return_msg['result'] = '0100'

    session.close()
    json_string = json.dumps(return_msg)
    return json_string
