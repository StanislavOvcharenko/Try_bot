from aiogram import types, Dispatcher
from app.create_bot import dp
from app.handlers.command_choice import command_choice_client, command_choice_admin


# @dp.message_handler()
async def invalidCommand(message: types.Message):
    # if not message.text.startswith("/"):
    if message.text[0::] not in command_choice_client and command_choice_admin:
        await message.reply("i dont understand you, please use commands")
        # return telegram menu

def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(invalidCommand)
