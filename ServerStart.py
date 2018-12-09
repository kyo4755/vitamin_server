from flask import Flask
from Database.database import init_db

app = Flask(__name__)

from UserManage import image, login, register, token
from Chatting import chat, translate
from Friends import friend
from SNS import sns
from Study import quiz, youglish
from Rekognition import rekognition


@app.route("/")
def hello_world():
    return "Hello, world!"


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', debug=True)
