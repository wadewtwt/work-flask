from flask import Flask
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy import text
import sys
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import sql

HOST = '139.224.60.242'  # 127.0.0.1/localhost
PORT = 3306
DATA_BASE = 'some-note'
USER = 'root'
PWD = '940327Wt!'
# DB_URI = f'数据库的名+驱动名://{USER}:{PWD}@{HOST}:{PORT}/{DATA_BASE}'
DB_URI = f'mysql+pymysql://{USER}:{PWD}@{HOST}:{PORT}/{DATA_BASE}'

app = Flask(__name__)
engine = create_engine(DB_URI)
Base = declarative_base(engine)
session = sessionmaker(engine)()


class Note(Base):
    __tablename__ = 't_note'
    id = Column(Integer, primary_key=True, autoincrement=True)
    account = Column(String(255))
    password = Column(Integer)


@app.route('/')
def hello_world():
    with Session() as session:
        p2 = Note(account='MySQL', password='SQL')
        session.add_all([p2])
        session.commit()

    return 'Hello World!112'


if __name__ == '__main__':
    Base.metadata.create_all()
    app.config.update(DEBUG=True)
    app.run()


@app.route('/users/<user_id>')
def user_info(user_id):
    # HOST = '139.224.60.242'  # 127.0.0.1/localhost
    # PORT = 3306
    # DATA_BASE = 'some-note'
    # USER = 'root'
    # PWD = '940327Wt!'
    # # DB_URI = f'数据库的名+驱动名://{USER}:{PWD}@{HOST}:{PORT}/{DATA_BASE}'
    # DB_URI = f'mysql+pymysql://{USER}:{PWD}@{HOST}:{PORT}/{DATA_BASE}'
    # engine = create_engine(DB_URI)
    # # 执行一个SQL
    # sql = 'select * from t_note;'
    # conn = engine.connect()
    # rs = conn.execute(text(sql))
    # print(rs.fetchone())

    print(type(user_id))
    return 'hello user{}'.format(user_id)
