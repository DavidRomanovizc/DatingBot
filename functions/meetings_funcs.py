from loader import bot
from utils.db_api import db_commands


async def get_meeting_data(telegram_id):
    user = await db_commands.select_meetings_user(telegram_id=telegram_id)

    user_name = user.get("username")
    meeting_description = user.get("meetings_description")

    return (
        user_name, meeting_description
    )


async def send_ques_meeting(chat_id, user_data, markup):
    await bot.send_message(chat_id=chat_id, text=f"{user_data[1]}\n\n"
                                                 f'<a href="https://t.me/{user_data[0]}">{user_data[0]}</a>',
                           reply_markup=markup)