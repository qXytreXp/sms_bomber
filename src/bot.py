import __init__
import handlers

from aiogram.utils import executor
from src.dispatcher import dp


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
