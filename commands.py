from sqlalchemy.exc import PendingRollbackError, IntegrityError
from models import session, Money, Subscribe
from money import Converter
import datetime

"""
Класс для получения информации о курсе доллара
"""
class InfoMoney():

    def money_info(self, user_id):         # Метод заносящий в базу информацию о курсе, дате запроса и id пользователя
        self.user_id = user_id
        money_today = Converter.get_price()  #Получаем курс
        date_now = datetime.datetime.now()    # Получаем дату
        date_now_format = date_now.strftime("%Y-%m-%d %H:%M:%S")       # форматирование даты
        money = Money(
            date=date_now_format,
            money=money_today,
            user_id=int(user_id)
        )

        session.add(money)

        try:
            session.commit()
            return True
        except IntegrityError:
            session.rollback()  # откатываем session.add(money)
            return False

    def show_money_all(self, user_current_id):    # Метод для получения истории запросов прользователя
        self.user_current_id = user_current_id
        all_money = session.query(Money).filter(Money.user_id == user_current_id)    # Фильтруем данные по id пользователя
        return all_money


"""
Класс для формирования подписки пользователя на рассылку 
"""
class SubscribeUsers():

    def add_subscribe(self, message):     # Метод добавляющий пользователя в таблицу подписки
        self.message = message
        subscribe = Subscribe(
            user_id=int(message.from_user.id)
        )

        session.add(subscribe)

        try:
            session.commit()
            return True
        except IntegrityError:
            session.rollback()
            return False

    def subscribe_all(self):                # Метод получающий всех подписанных пользователей
        all_subscribe_users = session.query(Subscribe).all()
        return all_subscribe_users






