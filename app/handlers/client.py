import sqlalchemy.exc
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from app.create_bot import bot, dp
from app.handlers.command_choice import command_choice_client
from app.keyboards import keyboard_client, choise_keyborads
from app.data_base.alchemy import AllClient, CafeMenu
from app.data_base import session
from app.handlers.admin import admins_id
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def commands_start(message: types.Message):
    if message.from_user.id in admins_id:
        await bot.send_message(message.from_user.id, command_choice_client["start"][1], reply_markup=choise_keyborads)
    else:
        await bot.send_message(message.from_user.id, command_choice_client["start"][1], reply_markup=keyboard_client)
        client = AllClient(client_id=message.from_user.id)
        try:
            session.add(client)
            session.commit()
        except sqlalchemy.exc.IntegrityError:
            pass
        except sqlalchemy.exc.PendingRollbackError:
            pass


async def time_work(message: types.Message):
    await bot.send_message(message.from_user.id, command_choice_client["Режим_работы"][1])
    await bot.send_message(message.from_user.id, text=message.from_user.id)


async def address_shop(message: types.Message):
    await bot.send_message(message.from_user.id, command_choice_client["Расположение"][1])


async def contact(message: types.Message):
    await bot.send_message(message.from_user.id, command_choice_client["Контакты"][1])
    await bot.send_message(message.from_user.id, command_choice_client["Контакты"][2])


async def menu(message: types.Message):
    my_menu = session.query(CafeMenu).all()
    for i in my_menu:
        inline_delete_button = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(
            text=f'Удалить {i.product_name}', callback_data=f'Удалить_{i.id}_{i.product_name}'))
        if message.from_user.id in admins_id:
            await bot.send_photo(message.from_user.id, i.photo_id, f'{i.product_name}\nОписание: {i.description}\n'
                                                                   f'Цена:{i.price}', reply_markup=inline_delete_button)
        else:
            await bot.send_photo(message.from_user.id, i.photo_id, f'{i.product_name}\nОписание: {i.description}\n'
                                                                   f'Цена:{i.price}')


async def delete_menu_instance(callback: types.CallbackQuery):
    my_instance = callback.data.split('_')

    session.query(CafeMenu).filter(CafeMenu.id == int(my_instance[1])).filter(
        CafeMenu.product_name == my_instance[2]).delete()
    session.commit()
    await callback.answer(text=f'Удалено: {my_instance[2]}')


# lambda x: x.data and x.data.startswith('Удалить_')


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(commands_start, commands=command_choice_client["start"][0])
    dp.register_message_handler(time_work, commands=command_choice_client["Режим_работы"][0])
    dp.register_message_handler(address_shop, commands=command_choice_client["Расположение"][0])
    dp.register_message_handler(contact, commands=command_choice_client["Контакты"][0])
    dp.register_message_handler(menu, commands=command_choice_client["Меню"])
    dp.register_callback_query_handler(delete_menu_instance, Text(startswith='Удалить_'))
