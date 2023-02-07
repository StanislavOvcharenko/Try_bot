from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

load_button = KeyboardButton("/Загрузить_товар")
delete_button = KeyboardButton("/Удалить_товар")

keyboard_admin = ReplyKeyboardMarkup(resize_keyboard=True)

keyboard_admin.add(load_button).add(delete_button)


choise_admin_keyborads = KeyboardButton("/Клавиатура_администратора")
choise_client_keyborads = KeyboardButton("/Клавиатура_клиента")

choise_keyborads = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)

choise_keyborads.add(choise_admin_keyborads).add(choise_client_keyborads)
