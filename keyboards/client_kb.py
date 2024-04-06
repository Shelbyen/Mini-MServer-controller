from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from other import create_callback_data, Commands


def create_choice_keyboard(a, page, is_last_page):
    keyboard_with_servers = InlineKeyboardMarkup()
    for i in a:
        keyboard_with_servers.add(
            InlineKeyboardButton(i[1], callback_data=create_callback_data(Commands.SERVER_INFO.value,
                                                                          server_id=i[0],
                                                                          c_info=page)))
    keyboard_with_servers.add(
        InlineKeyboardButton(('<-' if page > 0 else 'X'),
                             callback_data=create_callback_data(Commands.CHOICE_SERVER.value,
                                                                c_info=(page - 1 if page > 0 else '-1'))
                             ),
        InlineKeyboardButton("Назад", callback_data="menu"),
        InlineKeyboardButton(("->" if not is_last_page else "X"),
                             callback_data=create_callback_data(Commands.CHOICE_SERVER.value,
                                                                c_info=(page + 1 if not is_last_page else '-1'))
                             ))

    return keyboard_with_servers


def create_server_keyboard(server_id, l_p, server_is_start):
    server_keyboard = InlineKeyboardMarkup()
    server_keyboard.add(
        InlineKeyboardButton("Изменить имя", callback_data=create_callback_data(Commands.RENAME.value, server_id, l_p)),
        InlineKeyboardButton("Изменить описание",
                             callback_data=create_callback_data(Commands.EDIT_DESCRIPTION.value, server_id, l_p)))

    server_keyboard.add(InlineKeyboardButton("Редактировать моды",
                                             callback_data=create_callback_data(Commands.EDIT_MODS.value, server_id,
                                                                                l_p)))

    if not server_is_start:
        server_keyboard.add(InlineKeyboardButton("Запустить!",
                                                 callback_data=create_callback_data(Commands.START.value, server_id,
                                                                                    l_p)))
    else:
        server_keyboard.add(InlineKeyboardButton("Остановить!",
                                                 callback_data=create_callback_data(Commands.STOP.value, server_id,
                                                                                    l_p)))

    server_keyboard.add(
        InlineKeyboardButton("Назад", callback_data=create_callback_data(Commands.CHOICE_SERVER.value, c_info=l_p)))

    return server_keyboard


return_back = InlineKeyboardMarkup()
main_menu = InlineKeyboardMarkup()

return_back.add(InlineKeyboardButton("Назад", callback_data="menu"))

main_menu.add(
    InlineKeyboardButton("Список серверов", callback_data=create_callback_data(Commands.CHOICE_SERVER.value, c_info=0)))
