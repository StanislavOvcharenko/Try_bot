from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

time_work_button = KeyboardButton("/Режим_работы")
adress_shop_button = KeyboardButton("/Расположение")
contacts_button = KeyboardButton("/Контакты")
menu_button = KeyboardButton("/Меню")

keyboard_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)

keyboard_client.add(menu_button).add(time_work_button).add(adress_shop_button).insert(contacts_button)

