import asyncio
from aiogram import types
import logging
import sys
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.enums import ParseMode


from commands import register_user, select_user
from aiogram import Bot, Dispatcher, types


TOKEN = '6749688724:AAFeGakrYutaJGvWBpWVMY57h4hmq670_3o'

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start(message: Message):
    user = register_user(message)

    if user:
        await message.answer('Вы успешно зарегистрировались!')
    else:
        await message.answer('Вы уже зарегистрированы!')


@dp.message(Command('profile'))
async def show_profile(message: types.Message):
    user = select_user(message.from_user.id)

    await message.answer(f"Твой профиль\n"
                         f"Name: {user.name}\n"
                         f"Username: @{user.username}\n"
                         f"Admin: {'Да' if user.admin else 'Нет'}\n"
                         f"Time: {user.date}\n"
                         f"Course $: {user.money}"
                         )


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())