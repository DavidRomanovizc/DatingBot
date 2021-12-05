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
    photo = "https://sun9-47.userapi.com/impg/DYtebbMPsbK46Xx8bVHtKF3FCAfZ7-ws5q6mOg/hjPVNFAU0EU.jpg?size=800x400&quality=96&sign=043c95dfca1009f94d9ba8b8812dbdb1&type=album"
    photo_1 = "https://sun9-11.userapi.com/impg/FLc62X1Hp7WNW9p5w5jo3OnDEHbxF6hzsrMQwA/xaj4cTYYcYU.jpg?size=800x400&quality=96&sign=419b95999f4a74993fd46974d8cce309&type=album"
    await bot.send_photo(chat_id=call.from_user.id, photo=photo, caption="Нагрузка пользователями на бота в день: ")
    await bot.send_photo(chat_id=call.from_user.id, photo=photo_1, caption="Показатели по гендеру (мужчины/женщины): ")
    await asyncio.sleep(1)
    await call.message.answer("<b>❤️️ DATE_BOT</b> - платформа для поиска новых знакомств.\n\n"
                              "<b>🤝 Сотрудничество: </b>\n"
                              "Если у вас есть предложение о сотрудничестве, пишите сюда - "
                              "@DRomanovizc", reply_markup=inline_start)
