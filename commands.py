from sqlalchemy.exc import PendingRollbackError, IntegrityError
from user import session, User
from money import Converter
import datetime


def register_user(message):
    username = message.from_user.username if message.from_user.username else None
    money_today = Converter.get_price()
    user = User(
        id=int(message.from_user.id),
        username=username,
        name=message.from_user.full_name,
        date=datetime.datetime.now(),
        money=money_today
    )

    session.add(user)

    try:
        session.commit()
        return True
    except IntegrityError:
        session.rollback()  # откатываем session.add(user)
        return False


def select_user(user_id):
    user = session.query(User).filter(User.id == user_id).first()
    return user