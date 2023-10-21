import asyncio
import logging
import sys
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.enums import ParseMode
from money import Converter
from keyboards import keyboard

from commands import SubscribeUsers, InfoMoney
from config import TOKEN
from aiogram import Bot, Dispatcher, types, F




dp = Dispatcher()

bot = Bot(TOKEN) # токен бота

scheduler = AsyncIOScheduler()

info = InfoMoney()           # Создаём экземпляры классов
subscribe = SubscribeUsers()


@dp.message(CommandStart())   # Первое сообщение при старте котрое передаёт клавиатуру
async def command_start(message: Message):
    await message.answer(f'Приветствую, {message.from_user.username}', reply_markup=keyboard)


@dp.message(F.text.lower() == 'курс$')       # Запрашиваем курси и записываем данные запроса в базу
async def show_money(message: types.Message):
    user_id = int(message.from_user.id)
    money = info.money_info(user_id)
    await message.answer(f'{Converter.get_price()} p')


@dp.message(F.text.lower() == 'история')     # Сообщение об истории запросов
async def show_money_history(message: types.Message):
    money = info.show_money_all(message.from_user.id)    # Получаем данные по истории пользователя

    money_list = []    # инициализируем список

    for i in money:
        d = str(i.date)
        m = str(i.money)
        money_list.append(d)
        money_list.append(m)
        money_list.append('\n')         # формируем список из значений
    text = ' '.join(money_list)         # перебираем список в строку
    await bot.send_message(message.from_user.id, f" История Ваших запросов \n {text}") # выводим строку


async def money_subscribe(message: Message):    # функция рассылки сообщений подписанным пользователям
    subscribe_users = subscribe.subscribe_all()   # получаем всех подписавшихся пользователей
    for i in subscribe_users:             # В цикле получаем id каждого пользователя и вносим его в адресс рассылки
        id_user = i.user_id
        histori = info.money_info(id_user) # Заносим в базу информацию о запросе
        await bot.send_message(id_user, f'{Converter.get_price()} p') # Передаём в рассылке информацию о курсе


def schedule_jobs():       # Формируем задачу на рассылку с интервалом каждые 25 секунд
    scheduler.add_job(money_subscribe, "interval", seconds=25, args=(dp,))


@dp.message(F.text.lower() == 'подписка')        # Подписка на рассылку
async def spam(message: Message):
    list_sub = []                                  # пустой список для id подписанных пользователей
    for i in subscribe.subscribe_all():
        list_sub.append(i.user_id)                 # собираем список id пользователей подписанныйх на рассылку
    if message.from_user.id in list_sub:           # проводим проверку на наличие id пользователя в списке подписавшихся для исключения задвоения подписки
        await message.answer('Вы уже подписаны')
    else:
        sub = subscribe.add_subscribe(message)     # елси пользователя нет в списке то вносим его в базу на рассылку
        await message.answer(f'рассылка')


async def main() -> None:
    schedule_jobs()            # Инициализируем задачу
    scheduler.start()          # Стартуем задачу
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())