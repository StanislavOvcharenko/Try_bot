from aiogram.utils import executor
from create_bot import dp
from app.handlers import client, admin, other
from app.data_base.alchemy import Base, engine, Admins
from app.handlers.admin import admins_id
from app.data_base import session


async def on_startup(_):
    Base.metadata.create_all(engine)
    for ad in session.query(Admins).all():
        admins_id.append(ad.admin_telegram_id)

    print('Bot online')

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
# other must be last always, because have empty handler
other.register_handlers_other(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
