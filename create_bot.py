import os

from dotenv import load_dotenv

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from sqlalchemy import create_engine, MetaData, Table, Column
from sqlalchemy.types import Integer, String, Text

from server import Server

engine = create_engine("sqlite:///data/servers.db")
conn = engine.connect()
metadata = MetaData()

servers_db = Table(
    'servers',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),    Column('description', Text),
    Column('path', String)
)

metadata.create_all(engine)

# conn.execute(servers_db.insert().values([
#     {'id': 25565, 'name': 'Quadratny squad', 'description': 'Что то на сложном', 'path': r"C:\Servers\Quadratny squad"},
#     {'id': 25566, 'name': 'server_i', 'description': 'Похоже что ванила', 'path': r"C:\Servers\server_i"},
#     {'id': 25567, 'name': 'server_ic', 'description': 'Тот самый сервер с create((', 'path': r"C:\Servers\server_ic"}
# ]))

# print(conn.execute(select(servers_db.c.name, servers_db.c.id)).all())


load_dotenv()

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher(bot)
server = Server()
