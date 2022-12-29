from itertools import chain
from sqlalchemy import create_engine, insert, MetaData
from sqlalchemy import Column
from sqlalchemy import Integer

from sqlalchemy import String
from sqlalchemy.orm import declarative_base, sessionmaker

import constant

engine = create_engine(f'sqlite:///{constant.DBNAME}', connect_args={'check_same_thread': False}, echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    message_id = Column(Integer)
    name = Column(String(30))
    song = Column(String)


Base.metadata.create_all(engine)


def add_item(message_id, name, song):
    user = User(message_id=message_id, name=name, song=song)
    session.add(user)
    session.commit()


def get_items(message_id):
    songs = session.query(User.song).where(User.message_id == message_id)
    return iter(chain(*songs))


def len_items(message_id):
    stmt = session.query(User.song).where(User.message_id == message_id)
    return len(list(stmt))
