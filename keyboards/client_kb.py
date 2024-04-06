from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

return_back = InlineKeyboardMarkup()
main_menu = InlineKeyboardMarkup()

return_back.add(InlineKeyboardButton("Назад", callback_data="menu"))

main_menu.add(InlineKeyboardButton("Список серверов", callback_data="server_list"))
