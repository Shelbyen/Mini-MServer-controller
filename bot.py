from enum import Enum
from math import ceil

from aiogram import types
from aiogram.utils import executor
from sqlalchemy import select

from create_bot import dp, bot, server, conn, servers_db
from keyboards.client_kb import main_menu, return_back, create_server_keyboard, create_choice_keyboard
from other import decode_callback_data, Commands


async def on_startup(_):
    print('Бот вышел в онлайн')


@dp.message_handler(commands=['start'])
async def menu(message):
    await bot.send_message(message.from_user.id, "Бот для управления серверами!!!", reply_markup=main_menu)


@dp.callback_query_handler(text="menu")
async def menu(call):
    await call.message.edit_text("Бот для управления серверами!!!", reply_markup=main_menu)


@dp.callback_query_handler(text="running_servers")
async def running_servers(call: types.CallbackQuery):
    await call.message.delete()
    a = server.server_processes
    t = 'Запущенные сервера: \n'
    for i in a:
        t += i + '\n'
    await bot.send_message(call.from_user.id, t, reply_markup=return_back)


@dp.callback_query_handler(lambda c: c.data and decode_callback_data(c.data)[1] == Commands.CHOICE_SERVER.value)
async def choice_server(call: types.CallbackQuery):
    page = decode_callback_data(call.data)[2]
    all_servers = conn.execute(select(servers_db.c.id, servers_db.c.name)).all()
    if not 0 <= page <= ceil(len(all_servers) / 2):
        return False

    a = all_servers[page * 2: page * 2 + 2]
    is_last_page = page == ceil(len(all_servers) / 2) - 1
    await call.message.edit_text('Доступные сервера:',
                                 reply_markup=create_choice_keyboard(a, page, is_last_page))


@dp.callback_query_handler(lambda c: c.data and decode_callback_data(c.data)[1] == Commands.SERVER_INFO.value)
async def server_info(call: types.CallbackQuery):
    server_id, _, l_p = decode_callback_data(call.data)
    info = conn.execute(servers_db.select().where(servers_db.c.id == int(server_id))).first()
    t = 'Имя сервера: ' + info[1] + '\n'
    t += 'Статус: ' + ('Запущен!' if info[0] in server.server_processes else 'Не запущен!') + '\n'
    t += 'Описание: ' + info[2] + '\n'

    is_start = info[0] in server.server_processes
    await call.message.edit_text(t, reply_markup=create_server_keyboard(info[0], l_p, is_start))


@dp.callback_query_handler(lambda c: c.data and decode_callback_data(c.data)[1] == Commands.START.value)
async def start_command(call: types.CallbackQuery):
    server_id, _, l_p = decode_callback_data(call.data)
    await call.answer(server.start_server(
        conn.execute(servers_db.select().where(servers_db.c.id == server_id)).first()))
    await server_info(call)


@dp.callback_query_handler(lambda c: c.data and decode_callback_data(c.data)[1] == Commands.STOP.value)
async def stop_command(call: types.CallbackQuery):
    server_id, _, l_p = decode_callback_data(call.data)
    await call.answer(server.stop_server(
        conn.execute(servers_db.select().where(servers_db.c.id == server_id)).first()))
    await server_info(call)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
