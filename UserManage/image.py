from ServerStart import app
from flask import request
from Database.database import db_session
from Database.models import UserDetail, UserImage, SNSImage
import json


@app.route("/users/changePhoto", methods=['POST'])
def change_photo():
    session = db_session()
    return_msg = {'result': '0000', 'image': ''}

    if request.method == 'POST':
        id = request.form['id']
        image = request.files['image'].read()

        if id is None or len(id) == 0:
            return_msg['result'] = '0001'
            json_string = json.dumps(return_msg)
            return json_string

        if image is None:
            return_msg['result'] = '0002'
            json_string = json.dumps(return_msg)
            return json_string

        query = session.query(UserDetail) \
            .filter(UserDetail.id == id).all()

        for detail in query:
            if detail.image is None:
                query_id = session.query(UserImage.id).order_by(UserImage.id.desc()).first()
                if query_id is None:
                    img_id = 1
                else:
                    query_img_id = query_id[0]
                    img_id = int(query_img_id) + 1
                image_data = UserImage(str(img_id), image)
                session.add(image_data)
                detail.image = str(img_id)
                return_msg['image'] = str(img_id)
            else:
                query_image = session.query(UserImage)\
                    .filter(UserImage.id == detail.image).all()
                for q_img in query_image:
                    q_img.image = image
                return_msg['image'] = detail.image

        session.commit()

    else:
        return_msg['result'] = '0100'

    session.close()
    json_string = json.dumps(return_msg)
    return json_string


@app.route("/users/getPhoto", methods=['GET'])
def user_photo():
    session = db_session()
    id = request.args.get('id')
    if id is None or id == 'null':
        return 'fail'

    query = session.query(UserImage.image)\
        .filter(UserImage.id == id).first()
    img = query[0]

    session.close()
    return img


@app.route("/sns/getPhoto", methods=['GET'])
def sns_photo():
    session = db_session()
    id = request.args.get('id')
    if id is None or id == 'null':
        return 'fail'

    query = session.query(SNSImage.image)\
        .filter(SNSImage.index == id).first()
    img = query[0]

    session.close()
    return img
