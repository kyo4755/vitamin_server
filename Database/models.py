from sqlalchemy import Column, String, BLOB, Text, Integer, DateTime
from Database.database import Base


class UserDetail(Base):
    __tablename__ = 'user_detail'
    id = Column(String(20), primary_key=True)
    passwd = Column(String(20))
    phone_number = Column(String(20))
    name = Column(String(10))
    email = Column(String(30))
    nation = Column(String(10))
    location = Column(String(50))
    prefer_language = Column(String(100))
    status_msg = Column(String(100))
    image = Column(String(20))
    token = Column(String(500))

    def __init__(self, id, passwd, phone_number, name, email, nation, location, prefer_language):
        self.id = id
        self.passwd = passwd
        self.phone_number = phone_number
        self.name = name
        self.email = email
        self.nation = nation
        self.location = location
        self.prefer_language = prefer_language


class UserImage(Base):
    __tablename__ = 'user_image'
    id = Column(String(20), primary_key=True)
    image = Column(BLOB)

    def __init__(self, id, image):
        self.id = id
        self.image = image


class FriendsList(Base):
    __tablename__ = 'friends_list'
    id = Column(String(20), primary_key=True)
    friendId = Column(String(1000))

    def __init__(self, id):
        self.id = id


class ChatRoom(Base):
    __tablename__ = 'chat_room'
    index = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(String(20))
    room_num = Column(Integer)
    member = Column(String(1000))

    def __init__(self, id, room_num, member):
        self.id = id
        self.room_num = room_num
        self.member = member


class ChatRoomDetail(Base):
    __tablename__ = 'chat_room_detail'
    index = Column(Integer, primary_key=True, autoincrement=True)
    room_num = Column(Integer)
    id = Column(String(20))
    date = Column(DateTime)
    msg = Column(Text)

    def __init__(self, room_num, id, date, msg):
        self.room_num = room_num
        self.id = id
        self.date = date
        self.msg = msg


class SNSDetail(Base):
    __tablename__ = 'sns_detail'
    index = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(String(20))
    date = Column(DateTime)
    content_text = Column(Text)
    content_img = Column(String(20))

    def __init__(self, id, date, content_text, content_img):
        self.id = id
        self.date = date
        self.content_text = content_text
        self.content_img = content_img


class SNSImage(Base):
    __tablename__ = 'sns_image'
    index = Column(String(20), primary_key=True)
    image = Column(BLOB)

    def __init__(self, index, image):
        self.index = index
        self.image = image


class SNSComment(Base):
    __tablename__ = 'sns_comment'
    auin = Column(Integer, primary_key=True, autoincrement=True)
    index = Column(Integer)
    id = Column(String(20))
    date = Column(DateTime)
    comment = Column(Text)

    def __init__(self, index, id, date, comment):
        self.index = index
        self.id = id
        self.date = date
        self.comment = comment


class Translate(Base):
    __tablename__ = 'translate'
    index = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(String(20))
    before_msg = Column(Text)
    after_msg = Column(Text)

    def __init__(self, index, id, before_msg, after_msg):
        self.index = index
        self.id = id
        self.before_msg = before_msg
        self.after_msg = after_msg