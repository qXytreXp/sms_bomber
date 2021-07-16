import logging

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from mongoengine import connect

from src import config


logging.basicConfig(level=logging.INFO)

mongodb_connect = connect(
    db=config.MONGODB_DATABASE,
    alias='default',
    host=config.MONGODB_HOST,
    port=config.MONGODB_PORT,
    username=config.MONGODB_USERNAME,
    password=config.MONGODB_PASSWORD
)
storage = MemoryStorage()
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=storage)
