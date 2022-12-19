from utils import get_config, save_config, str2file, check_int
from aiogram import Bot, Dispatcher, types, filters, executor
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.contrib.fsm_storage.mongo import MongoStorage
from db import DataBase


config_filename = "config.json"
config = get_config(config_filename)
db = DataBase(config["db_url"], config["db_name"])
bot = Bot(token=config["bot_token"], parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MongoStorage(db_name=config["db_name"], uri=config["db_url"]))
owners_filter = filters.IDFilter(user_id=config["owners"])

class UsersMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        super(UsersMiddleware, self).__init__()

count = db.get_users_count()
print(count)
@dp.message_handler(owners_filter, commands=["start"])
async def main(message: types.Message):
    try:
        for user in db.get_user():
            try:
                await bot.send_message(user['user_id'], text='test')
            except Exception as a:
                print(a, "	|	", user['user_id'])
                db.delete_user(user['user_id'])
    except Exception as a:
        print(a)

dp.middleware.setup(UsersMiddleware())

if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=False)
