from sqlalchemy import create_engine, Column, Integer, Boolean, String, Float, DateTime
from sqlalchemy.orm import scoped_session, declarative_base, sessionmaker
import datetime


engine = create_engine("sqlite:///test.db", echo=True)

session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = session.query_property()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    name = Column(String)
    money = Column(Float)
    date = Column(DateTime, autoincrement=True)
    admin = Column(Boolean, default=False)


# class Money(Base):
#     __tablename__ = 'money'
#
#     id = Column(Integer, primary_key=True)
#     money = Column(Float)
#     # date = Column(DateTime)


Base.metadata.create_all(bind=engine)