import os
from dotenv import load_dotenv

from aiogram import Bot
from aiogram.dispatcher import Dispatcher

from server import Server

load_dotenv()

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher(bot)
server = Server()
