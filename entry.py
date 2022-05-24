from config import BOT_TOKEN

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher


bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot, storage = MemoryStorage())
