from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql+pymysql://root:@13.124.62.147:2000/vitamin?charset=utf8', convert_unicode=False)
db_session = sessionmaker(bind=engine)
db_session.configure(bind=engine)

Base = declarative_base()


def init_db():
    import Database.models
    Base.metadata.create_all(engine)