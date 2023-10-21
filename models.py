from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import scoped_session, declarative_base, sessionmaker

"""
Подключаем базу и формируем модели
по уму надо бы взять асинхронный вариант алхимии и базу постгрес, 
но ввиду того что на рабочем компе нет возможности её использовать (нет прав администратора) пусть будет скулайт
"""


engine = create_engine("sqlite:///test.db", echo=True)

session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = session.query_property()


class Money(Base):
    __tablename__ = 'moneys'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    money = Column(Float)
    date = Column(String)


class Subscribe(Base):
    __tablename__ = 'subscribers'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)


Base.metadata.create_all(bind=engine)