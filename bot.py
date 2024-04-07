from math import ceil

from aiogram import types
from aiogram.utils import executor
from sqlalchemy import select

from create_bot import dp, bot, server_controller, conn, servers_db
from keyboards.client_kb import main_menu, return_back, create_server_keyboard, create_choice_keyboard
from other import decode_callback_data, Commands, ServerStatus, name_server_status


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
    a = server_controller.server_processes
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


@dp.callback_query_handler(
    lambda c: c.data and decode_callback_data(c.data)[1] in [Commands.SERVER_INFO.value])
async def send_server_info(call: types.CallbackQuery):
    server_id, _, l_p = decode_callback_data(call.data)
    info = conn.execute(servers_db.select().where(servers_db.c.id == int(server_id))).first()
    if info[0] in server_controller.server_processes:
        server_status = server_controller.server_processes[info[0]].status
    else:
        server_status = -1
    t = 'Имя сервера: ' + info[1] + '\n'
    t += 'Статус: ' + (name_server_status[server_status]) + '\n'
    if info[0] in server_controller.server_processes:
        if server_status == ServerStatus.READY.value:
            server_info = server_controller.get_server_info(info)
            t += f'Текущий TPS: {server_info["TPS"][0]}' + '\n'
            t += f'Память: {server_info["TPS"][1]} (Максимальная: {server_info["TPS"][2]})' + '\n'
            t += f'Игроки {server_info["players"][0]}/{server_info["players"][1]}:' + '\n'
            for i in server_info['players'][2]:
                t += '\t' + i + '\n'
    t += 'Описание: ' + info[2] + '\n'

    await call.message.edit_text(t, reply_markup=create_server_keyboard(info[0], l_p, server_status))


@dp.callback_query_handler(lambda c: c.data and decode_callback_data(c.data)[1] == Commands.START.value)
async def start_command(call: types.CallbackQuery):
    server_id, _, l_p = decode_callback_data(call.data)
    await call.answer(server_controller.start_server(
        conn.execute(servers_db.select().where(servers_db.c.id == server_id)).first()))
    await send_server_info(call)


@dp.callback_query_handler(lambda c: c.data and decode_callback_data(c.data)[1] == Commands.STOP.value)
async def stop_command(call: types.CallbackQuery):
    server_id, _, l_p = decode_callback_data(call.data)
    await call.answer(server_controller.stop_server(
        conn.execute(servers_db.select().where(servers_db.c.id == server_id)).first()))
    await send_server_info(call)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
