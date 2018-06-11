from ServerStart import app
from flask import request
from Database.database import db_session
from Database.models import SNSDetail, SNSImage, SNSComment, UserDetail
import json


@app.route("/sns/getList", methods=['POST'])
def sns_get_list():
    session = db_session()
    return_msg = {'result': '0000', 'sns_list': []}

    if request.method == 'POST':
        start_num = request.form['startNum']
        end_num = request.form['endNum']

        if start_num is None or len(start_num) == 0:
            return_msg['result'] = '0001'
            json_string = json.dumps(return_msg)
            return json_string

        if end_num is None or len(end_num) == 0:
            return_msg['result'] = '0002'
            json_string = json.dumps(return_msg)
            return json_string

        int_start_num = int(start_num) - 1
        int_end_num = int(end_num) - 1

        query = session.query(SNSDetail).order_by(SNSDetail.date.desc()).all()[int_start_num:int_end_num]

        if query is None:
            return_msg['result'] = '0003'
        else:
            for detail in query:
                query_user = session.query(UserDetail)\
                    .filter(UserDetail.id == detail.id).first()

                query_count = session.query(SNSComment)\
                    .filter(SNSComment.index == detail.index).count()

                if query_user is None:
                    return_msg['result'] = '0010'
                else:
                    sns_dict = {'index': detail.index,
                                'id': detail.id,
                                'name': query_user.name,
                                'user_image': query_user.image,
                                'prefer_language': query_user.prefer_language,
                                'date': detail.date,
                                'content_text': detail.content_text,
                                'content_image': detail.content_image,
                                'comment_count': query_count
                                }
                    return_msg['sns_list'].append(sns_dict)
    else:
        return_msg['result'] = '0100'

    session.close()
    json_string = json.dumps(return_msg)
    return json_string


@app.route("/sns/insertContent", methods=['POST'])
def sns_insert_content():
    session = db_session()
    return_msg = {'result': '0000'}

    if request.method == 'POST':
        id = request.form['id']
        date = request.form['date']
        content_text = request.form['content_text']
        content_image = request.files['content_image'].read()

        if id is None or len(id) == 0:
            return_msg['result'] = '0001'
            json_string = json.dumps(return_msg)
            return json_string

        if date is None or len(date) == 0:
            return_msg['result'] = '0002'
            json_string = json.dumps(return_msg)
            return json_string

        if content_text is None or len(content_text) == 0:
            return_msg['result'] = '0003'
            json_string = json.dumps(return_msg)
            return json_string

        str_img = "none"
        if content_image is not None:
            query = session.query(SNSImage.index)\
                .order_by(SNSImage.index.desc()).first()

            if query is None:
                str_img = "1"
            else:
                str_img = str(int(query[0]) + 1)

            s = SNSImage(str_img, content_image)
            session.add(s)

        t = SNSDetail(id, date, content_text, str_img)
        session.add(t)
        session.commit()

    else:
        return_msg['result'] = '0100'

    session.close()
    json_string = json.dumps(return_msg)
    return json_string


@app.route("/sns/insertComment", methods=['POST'])
def sns_insert_comment():
    session = db_session()
    return_msg = {'result': '0000'}

    if request.method == 'POST':
        index = request.form['index']
        id = request.form['id']
        date = request.form['date']
        msg = request.form['msg']

        if index is None or len(index) == 0:
            return_msg['result'] = '0001'
            json_string = json.dumps(return_msg)
            return json_string

        if id is None or len(id) == 0:
            return_msg['result'] = '0002'
            json_string = json.dumps(return_msg)
            return json_string

        if date is None or len(date) == 0:
            return_msg['result'] = '0003'
            json_string = json.dumps(return_msg)
            return json_string

        if msg is None or len(msg) == 0:
            return_msg['result'] = '0004'
            json_string = json.dumps(return_msg)
            return json_string

        t = SNSComment(index, id, date, msg)
        session.add(t)
        session.commit()

    else:
        return_msg['result'] = '0100'

    session.close()
    json_string = json.dumps(return_msg)
    return json_string


@app.route("/sns/getCommentList", methods=['POST'])
def sns_get_comment_list():
    session = db_session()
    return_msg = {'result': '0000', 'sns_comment_list': []}

    if request.method == 'POST':
        index = request.form['index']

        if index is None or len(index) == 0:
            return_msg['result'] = '0001'
            json_string = json.dumps(return_msg)
            return json_string

        query = session.query(SNSComment)\
            .filter(SNSComment.index == index).all()

        if query is None:
            return_msg['result'] = '0010'

        for detail in query:
            query_user = session.query(UserDetail)\
                .filter(UserDetail.id == detail.id).first()

            if query_user is None:
                return_msg['result'] = '0011'
            else:
                comment_dict = {'id': detail.id,
                                'name': query_user.name,
                                'user_image': query_user.image,
                                'date': detail.date,
                                'comment': detail.comment,
                                }

                return_msg['sns_comment_list'].append(comment_dict)

    else:
        return_msg['result'] = '0100'

    session.close()
    json_string = json.dumps(return_msg)
    return json_string


@app.route("/sns/getFriendSNSList", methods=['POST'])
def sns_get_friend_list():
    session = db_session()
    return_msg = {'result': '0000', 'sns_list': []}

    if request.method == 'POST':
        id = request.form['id']

        if id is None or len(id) == 0:
            return_msg['result'] = '0001'
            json_string = json.dumps(return_msg)
            return json_string

        query = session.query(SNSDetail)\
            .filter(SNSDetail.id == id).order_by(SNSDetail.date).all()

        if query is None:
            return_msg['result'] = '0010'
        else:
            for detail in query:
                query_count = session.query(SNSComment)\
                    .filter(SNSComment.index == detail.index).count()

                sns_dict = {'index': detail.index,
                            'date': detail.date,
                            'content_text': detail.content_text,
                            'content_image': detail.content_image,
                            'comment_count': query_count}

                return_msg['sns_list'].append(sns_dict)

        query_user = session.query(UserDetail)\
            .filter(UserDetail.id == id).first()

        if query_user is None:
            return_msg['result'] = '0011'
        else:
            return_msg['name'] = query_user.name
            return_msg['image'] = query_user.image

    else:
        return_msg['result'] = '0100'

    session.close()
    json_string = json.dumps(return_msg)
    return json_string
