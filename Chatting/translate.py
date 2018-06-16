from ServerStart import app
from flask import request
from Database.database import db_session
from Database.models import Translate
import json
import urllib.request, urllib.parse

detect_url = 'https://openapi.naver.com/v1/papago/detectLangs'
detect_client_id = 'sq0navEyQy58qJn4Xv9_'
detect_client_secret = 'Hn1_zUEibX'

papago_url = 'https://openapi.naver.com/v1/language/translate'
papago_client_id = 'jdq4Yxp8nmfFUzIpUiFa'
papago_client_secret = 'JPH7dtxmMm'


@app.route("/translate", methods=['GET'])
def translate():
    session = db_session()
    return_msg = {'result': '0000', 'translate_msg': ''}

    if request.method == 'GET':
        id = request.args.get('id')
        msg = request.args.get('msg')

        if id is None or len(id) == 0:
            return_msg['result'] = '0001'
            json_string = json.dumps(return_msg)
            return json_string

        if msg is None or len(msg) == 0:
            return_msg['result'] = '0001'
            json_string = json.dumps(return_msg)
            return json_string

        enc_text = urllib.parse.quote(msg)
        detect_data = "query=" + enc_text

        detect_request = urllib.request.Request(detect_url)
        detect_request.add_header("X-Naver-Client-Id", detect_client_id)
        detect_request.add_header("X-Naver-Client-Secret", detect_client_secret)

        detect_response = urllib.request.urlopen(detect_request, data=detect_data.encode("utf-8"))
        detect_res_code = detect_response.getcode()

        if detect_res_code == 200:
            detect_response_body = json.loads(detect_response.read().decode('utf-8'))
            from_nation = detect_response_body['langCode']

            if from_nation == 'ko':
                to_nation = 'en'
            else:
                to_nation = 'ko'

            trans_data = "source=" + from_nation + "&target=" + to_nation + "&text=" + enc_text

            trans_request = urllib.request.Request(papago_url)
            trans_request.add_header("X-Naver-Client-Id", detect_client_id)
            trans_request.add_header("X-Naver-Client-Secret", detect_client_secret)

            trans_response = urllib.request.urlopen(trans_request, data=trans_data.encode("utf-8"))
            trans_res_code = trans_response.getcode()

            if trans_res_code == 200:
                trans_response_body = json.loads(trans_response.read().decode('utf-8'))
                return_msg['translate_msg'] = trans_response_body['message']['result']['translatedText']

            else:
                return_msg['result'] = '0011'
        else:
            return_msg['result'] = '0010'

    else:
        return_msg['result'] = '0100'

    session.close()
    json_string = json.dumps(return_msg)
    return json_string

