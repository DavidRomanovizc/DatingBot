from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from keyboards.inline.necessary_links_inline import necessary_links_keyboard
from loader import bot, logger
from utils.db_api import db_commands


class LinkCheckMiddleware(BaseMiddleware):

    def __init__(self):
        super(LinkCheckMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        if message.chat.type == types.ChatType.PRIVATE:
            links_db = await db_commands.select_all_links()
            links_ids = [i["telegram_link_id"] for i in links_db]
            count = 0
            try:
                for i in links_ids:
                    check = await bot.get_chat_member(chat_id=i, user_id=message.from_user.id)
                    if check.status != 'left':
                        count += 1

                if len(links_ids) != count:
                    await message.answer('Вы подписались не на все каналы! Чтобы продолжить пользоваться ботом, '
                                         'подпишитесь! Ссылки ниже: ',
                                         reply_markup=await necessary_links_keyboard(telegram_id=message.from_user.id,
                                                                                     links_db=links_db))
                    raise BaseException
            except Exception as err:
                logger.error(err)
                pass
