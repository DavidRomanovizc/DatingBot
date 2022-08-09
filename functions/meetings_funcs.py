from keyboards.inline.meeting_inline import reaction_meetings_keyboard
from loader import bot
from utils.db_api import db_commands


async def get_meeting_data(telegram_id):
    user = await db_commands.select_meetings_user(telegram_id=telegram_id)

    user_name = user.get("username")
    meeting_description = user.get("meetings_description")
    user_status = user.get("status")

    return (
        user_name, meeting_description, user_status
    )


async def create_ques_meeting(state, random_user, chat_id):
    markup = await reaction_meetings_keyboard()
    user_data = await get_meeting_data(random_user)
    await send_ques_meeting(chat_id=chat_id, user_data=user_data, markup=markup)
    await state.update_data(data={'questionnaire_owner': random_user})


async def send_ques_meeting(chat_id, user_data, markup):
    await bot.send_message(chat_id=chat_id, text=f"{user_data[1]}\n\n"
                                                 f'<a href="https://t.me/{user_data[0]}">{user_data[0]}</a>',
                           reply_markup=markup)
