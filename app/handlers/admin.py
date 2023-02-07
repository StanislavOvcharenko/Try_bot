import os

import sqlalchemy.exc
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from app.create_bot import dp, bot
from app.handlers.command_choice import command_choice_admin
from app.data_base.alchemy import Admins, CafeMenu
from app.data_base import session
from app.keyboards import keyboard_admin, keyboard_client


class AddAdmin(StatesGroup):
    last_name = State()
    manager_id = State()


class FSMadmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


admins_id = []


# SuperAdmin add admins(managers)
async def start_add_admin(message: types.Message):
    if int(message.from_user.id) == int(os.getenv('ID')):
        await AddAdmin.last_name.set()
        await message.reply("Укажите фамилию сотрудника")


async def add_last_name_admin(message: types.Message, state: FSMContext):
    if int(message.from_user.id) == int(os.getenv('ID')):
        async with state.proxy() as data:
            data['last_name'] = str(message.text)
        await AddAdmin.next()
        await message.reply("Укажите ID сотрудника")


async def add_id_admin(message: types.Message, state: FSMContext):
    if int(message.from_user.id) == int(os.getenv('ID')):
        try:
            async with state.proxy() as data:
                data['admin_id'] = int(message.text)

            async with state.proxy() as data:
                if data['admin_id'] not in admins_id:
                    admins_id.append(data['admin_id'])
        except ValueError:
            await message.reply('error')

        async with state.proxy() as data:
            try:
                add_admin = Admins(admin_last_name=data['last_name'], admin_telegram_id=data['admin_id'])
                session.add(add_admin)
                session.commit()
            except sqlalchemy.exc.IntegrityError:
                await message.reply('Пользователь уже был добавлен')
                session.rollback()
        await state.finish()


# Admins add goods
async def start_admin(message: types.Message):
    if int(message.from_user.id) in admins_id:
        await FSMadmin.photo.set()
        await message.reply("Загрузите фотографию")


async def cancel_admin_handlers(message: types.Message, state: FSMContext):
    if int(message.from_user.id) in admins_id:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('OK')


async def load_photo(message: types.Message, state: FSMContext):
    if int(message.from_user.id) in admins_id:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMadmin.next()
        await message.reply("Введите название")





async def load_name(message: types.Message, state: FSMContext):
    if int(message.from_user.id) in admins_id:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMadmin.next()
        await message.reply("Введите описание")


async def load_description(message: types.Message, state: FSMContext):
    if int(message.from_user.id) in admins_id:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMadmin.next()
        await message.reply("Введите цену")


async def load_price(message: types.Message, state: FSMContext):
    if int(message.from_user.id) in admins_id:
        async with state.proxy() as data:
            data['price'] = float(message.text)

        async with state.proxy() as data:
            menu = CafeMenu(photo_id=data['photo'], product_name=data['name'],
                            description=data['description'], price=data['price'])
            session.add(menu)
            session.commit()
        await state.finish()



async def send_admin_keyboards(message: types.Message):
    if message.from_user.id in admins_id:
        await bot.send_message(message.from_user.id, 'admin', reply_markup=keyboard_admin)


async def send_client_keyboards(message: types.Message):
    await bot.send_message(message.from_user.id, 'client', reply_markup=keyboard_client)


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(start_admin, commands=command_choice_admin['Загрузить'][0], state=None)
    dp.register_message_handler(cancel_admin_handlers, state="*", commands=command_choice_admin['Отмена'][0])
    dp.register_message_handler(cancel_admin_handlers, Text(equals=command_choice_admin['Отмена'][0], ignore_case=True),
                                state="*")
    dp.register_message_handler(load_photo, content_types=["photo"], state=FSMadmin.photo)
    dp.register_message_handler(load_name, state=FSMadmin.name)
    dp.register_message_handler(load_description, state=FSMadmin.description)
    dp.register_message_handler(load_price, state=FSMadmin.price)
    dp.register_message_handler(start_add_admin, commands=command_choice_admin['Добавить_админа'][0], state=None)
    dp.register_message_handler(add_last_name_admin, state=AddAdmin.last_name)
    dp.register_message_handler(add_id_admin, state=AddAdmin.manager_id)
    dp.register_message_handler(send_admin_keyboards, commands=command_choice_admin['Клавиатура_администратора'])
    dp.register_message_handler(send_client_keyboards, commands=command_choice_admin['Клавиатура_клиента'])
