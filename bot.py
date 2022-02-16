from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import BOT_TOKEN 

import keyboard as kb

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_bot(message: types.Message):
    await bot.send_message(message.from_user.id, f"Привет {message.from_user.first_name}, на связи Информатор-бот!", reply_markup=kb.mainMenuParent)

@dp.message_handler()
async def bot_message(message: types.Message):

    if message.text == "Меню":        
        await bot.send_message(message.from_user.id, "Главное меню", reply_markup=kb.mainMenu)
    
    elif message.text == "Поиск":
         await bot.send_message(message.from_user.id, "Поиск мест", reply_markup=kb.searchMenu)

    elif message.text == "Рейтинг":
         await bot.send_message(message.from_user.id, "Способ просмотра рейтинга", reply_markup=kb.searchSubMenu)

    elif message.text == "Категории":
         await bot.send_message(message.from_user.id, "Категории поиска", reply_markup=kb.categoryMenu)
        
    elif message.text == "Настройки":
         await bot.send_message(message.from_user.id, "Выберите нужные настройки", reply_markup=kb.optionsMenu)

    elif message.text == "Назад":
         await bot.send_message(message.from_user.id, "Возврат в главное меню", reply_markup=kb.mainMenu)
    

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates = True)