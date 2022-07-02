from functions.get_data_func import get_data
from functions.send_form_func import send_questionnaire
from keyboards.inline.questionnaires_inline import questionnaires_keyboard
from utils.db_api import db_commands


async def create_questionnaire(form_owner, chat_id, add_text=None, monitoring=False):
    user_db = await db_commands.select_user(form_owner)
    markup = await questionnaires_keyboard(target_id=form_owner, monitoring=monitoring)
    user_data = await get_data(form_owner)
    await send_questionnaire(chat_id=chat_id, user_data=user_data, markup=markup, add_text=add_text, user_db=user_db,
                             monitoring=monitoring)


async def create_questionnaire_reciprocity(liker, chat_id, add_text=None, user_db=None):
    user_data = await get_data(liker)
    await send_questionnaire(chat_id=chat_id, user_data=user_data, add_text=add_text, user_db=user_db)