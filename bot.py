from math import ceil

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from sqlalchemy import select

from create_bot import dp, bot, server, conn, servers_db
from keyboards.client_kb import main_menu, return_back


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


@dp.callback_query_handler(lambda c: c.data and c.data.startswith("*b"))
async def choice_server(call: types.CallbackQuery):
    page = int(call.data[2:])
    all_servers = conn.execute(select(servers_db.c.id, servers_db.c.name)).all()
    if not 0 <= page <= ceil(len(all_servers) / 5):
        return False

    a = all_servers[page * 2: page * 2 + 2]
    keyboard_with_servers = InlineKeyboardMarkup()
    for i in a:
        keyboard_with_servers.add(InlineKeyboardButton(i[1], callback_data=f'#{page}+{i[0]}'))

    keyboard_with_servers.add(InlineKeyboardButton("<-", callback_data=f"*b{page - 1}"),
                              InlineKeyboardButton("Назад", callback_data="menu"),
                              InlineKeyboardButton("->", callback_data=f"*b{page + 1}"))

    await call.message.edit_text('Доступные сервера:', reply_markup=keyboard_with_servers)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith("#"))
async def server_info(call: types.CallbackQuery):
    await call.message.delete()
    info = conn.execute(servers_db.select().where(servers_db.c.id == int(call.data.split('+')[1]))).first()
    t = 'Имя сервера: ' + info[1] + '\n'
    t += 'Статус: ' + ('Запущен!' if info[0] in server.server_processes else 'Не запущен!') + '\n'
    t += 'Описание: ' + info[2] + '\n'
    server_keyboard = InlineKeyboardMarkup()
    server_keyboard.add(InlineKeyboardButton("Изменить имя", callback_data=f'!1{info[0]}'),
                        InlineKeyboardButton("Изменить описание", callback_data=f'!2{info[0]}'))

    server_keyboard.add(InlineKeyboardButton("Редактировать моды", callback_data=f'!3{info[0]}'))

    if info[0] not in server.server_processes:
        server_keyboard.add(InlineKeyboardButton("Запустить!", callback_data=f'@{info[0]}'))
    else:
        server_keyboard.add(InlineKeyboardButton("Остановить!", callback_data=f'%{info[0]}'))

    server_keyboard.add(InlineKeyboardButton("Назад", callback_data=f'*b{call.data[1:].split("+")[0]}'))
    await bot.send_message(call.from_user.id, t, reply_markup=server_keyboard)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith("@"))
async def start_command(call: types.CallbackQuery):
    await call.answer(server.start_server(
        conn.execute(servers_db.select().where(servers_db.c.id == int(call.data[1:]))).first()))


@dp.callback_query_handler(lambda c: c.data and c.data.startswith("%"))
async def stop_command(call: types.CallbackQuery):
    await call.answer(server.stop_server(
        conn.execute(servers_db.select().where(servers_db.c.id == int(call.data[1:]))).first()))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
