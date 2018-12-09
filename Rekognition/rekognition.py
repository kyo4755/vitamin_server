from ServerStart import app
from flask import request
from Database.database import db_session
from Database.models import UserDetail, UserImage
import boto3, json


@app.route("/recognition/compare", methods=['POST'])
def rekognition():
    session = db_session()
    return_msg = {'result': '0000', 'content': []}

    if request.method == 'POST':
        id = request.form['id']
        compared_img = request.files['image'].read()

        if id is None or len(id) == 0:
            return_msg['result'] = '0001'
            json_string = json.dumps(return_msg)
            return json_string

        if compared_img is None:
            return_msg['result'] = '0002'
            json_string = json.dumps(return_msg)
            return json_string

        client = boto3.client('rekognition')
        query = session.query(UserImage).all()

        for detail in query:
            print(id + " || " + detail.id)
            if detail.id == id:
                continue

            target_img = open(detail.image, 'rb').read()

            compare_res = client.compare_faces(
                SourceImage={
                    'Bytes': compared_img
                },
                TargetImage={
                    'Bytes': target_img
                },
                SimilarityThreshold=20
            )

            for match in compare_res['FaceMatches']:
                detailQuery = session.query(UserDetail).filter(UserDetail.image == detail.id).first()

                contents = {
                    "id": detailQuery.id,
                    "name": detailQuery.name,
                    "similarity": round(match['Similarity']),
                    "image": detailQuery.image
                }

                return_msg['content'].append(contents)

                break

    else:
        return_msg['result'] = '0100'

    session.close()
    json_string = json.dumps(return_msg)
    return json_string

