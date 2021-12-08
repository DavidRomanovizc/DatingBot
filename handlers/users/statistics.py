from keyboards.inline.main_menu import inline_start
from aiogram.types import CallbackQuery
from loader import dp, db, bot
import asyncio


@dp.callback_query_handler(text_contains="statistics")
async def get_inst(call: CallbackQuery):
    count_users = await db.count_users()
    await call.answer(cache_time=60)
    await call.message.edit_text(f"<b>💻 Статистика: </b>\n\n"
                                 f"└Сейчас в нашем боте <b>{count_users} пользователей</b>"
                                 f"└Дата создания бота - <b>10.08.2021</b>"
                                 )
    photo = "https://sun9-61.userapi.com/impg/Vz77VNXBjaNFFsr4-E07tjuHXu305GubZ_MJWA/hUiQ16DFuTU.jpg?size=800x400&quality=96&sign=ffbfe0b11238b9da1432b7919869fedf&type=album"
    photo_1 = "https://sun9-69.userapi.com/impg/TNeTmZN9VKO1jdUPQXWCmP7cHN7Jg-Rsl53smQ/7KCMcEA3-qk.jpg?size=800x400&quality=96&sign=386d4199a1c5f77286d233b4ea7a972c&type=album"
    await bot.send_photo(chat_id=call.from_user.id, photo=photo, caption="Нагрузка пользователями на бота в день: ")
    await bot.send_photo(chat_id=call.from_user.id, photo=photo_1, caption="Показатели по гендеру (мужчины/женщины): ")
    await asyncio.sleep(1)
    await call.message.answer("<b>❤️️ DATE_BOT</b> - платформа для поиска новых знакомств.\n\n"
                              "<b>🤝 Сотрудничество: </b>\n"
                              "Если у вас есть предложение о сотрудничестве, пишите сюда - "
                              "@DRomanovizc", reply_markup=inline_start)
