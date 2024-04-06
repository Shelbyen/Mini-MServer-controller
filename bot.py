from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from create_bot import dp, bot, server
from keyboards.client_kb import main_menu, return_back


async def on_startup(_):
    print('Бот вышел в онлайн')


@dp.message_handler(commands=['start'])
async def menu(message):
    await bot.send_message(message.from_user.id, "Бот для управления серверами!!!", reply_markup=main_menu)


@dp.callback_query_handler(text="menu")
async def menu(call):
    await call.message.delete()
    await bot.send_message(call.from_user.id, "Бот для управления серверами!!!", reply_markup=main_menu)


@dp.callback_query_handler(text="running_servers")
async def running_servers(call: types.CallbackQuery):
    await call.message.delete()
    a = server.server_processes
    t = 'Запущенные сервера: \n'
    for i in a:
        t += i + '\n'
    await bot.send_message(call.from_user.id, t, reply_markup=return_back)


@dp.callback_query_handler(text='server_list')
async def choice_server(call: types.CallbackQuery):
    await call.message.delete()
    a = server.get_servers()
    keyboard_with_servers = InlineKeyboardMarkup()
    for i in a:
        if i not in server.server_processes:
            keyboard_with_servers.add(InlineKeyboardButton(i, callback_data=f'#{i}'))
    keyboard_with_servers.add(InlineKeyboardButton("Назад", callback_data="menu"))
    await bot.send_message(call.from_user.id, 'Доступные сервера:', reply_markup=keyboard_with_servers)


@dp.callback_query_handler(lambda c: c.data.startswith("#"))
async def server_info(call: types.CallbackQuery):
    await call.message.delete()
    t = f'Имя сервера: {call.data[1:]} \n \n'
    t += f'Текущий статус: {"Запущен" if call.data[1:] in server.server_processes else "Не запущен"}\n'
    t += server.get_servers()[call.data[1:]] + '\n'
    server_keyboard = InlineKeyboardMarkup()
    if call.data[1:] not in server.server_processes:
        server_keyboard.add(InlineKeyboardButton("Запустить!", callback_data=f'@{call.data[1:]}'))
    else:
        server_keyboard.add(InlineKeyboardButton("Остановить!", callback_data=f'%{call.data[1:]}'))
    server_keyboard.add(InlineKeyboardButton("Назад", callback_data="menu"))
    await bot.send_message(call.from_user.id, t, reply_markup=server_keyboard)


@dp.callback_query_handler(lambda c: c.data.startswith("@"))
async def start_command(call: types.CallbackQuery):
    await bot.send_message(call.from_user.id, server.start_server(call.data[1:]))
    await menu(call)


@dp.callback_query_handler(lambda c: c.data.startswith("%"))
async def stop_command(call: types.CallbackQuery):
    await bot.send_message(call.from_user.id, server.stop_server(call.data[1:]))
    await menu(call)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
