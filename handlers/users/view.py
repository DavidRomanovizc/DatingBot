from hashlib import new
from aiogram.dispatcher import FSMContext
from aiogram import types
import random

from aiogram.types import message, CallbackQuery

from loader import dp, bot
from keyboards.inline.view_profile_keyboard import generate_keyboard
from states.view_p import ViewStates

# юзаю словарь, LOL
lst_of_id = [644475705, 929848338, 1]
datas = {
    644475705: {
        "like": 0,
        "dislike": 0,
        "name": "Bodya",
        "age": "2",
        "nationality": "3",
        "education": "4",
        "town": "5",
        "car": "6",
        "own_home": "7",
        "hobbies": "8",
        "child": "9"
    },
    929848338: {
        "like": 0,
        "dislike": 0,
        "name": "Kolya",
        "age": "8",
        "nationality": "7",
        "education": "6",
        "town": "5",
        "car": "4",
        "own_home": "3",
        "hobbies": "2",
        "child": "1"
    },
    1: {
        "like": 0,
        "dislike": 0,
        "name": "fdsfsdfsfd",
        "age": "8",
        "nationality": "7",
        "education": "6",
        "town": "5",
        "car": "4",
        "own_home": "3",
        "hobbies": "2",
        "child": "1"
    }
}

RESPONCE_TEXT = """
Доступные анкеты
----------------
Имя: {}
Возраст: {}
Национальность: {}
Образование: {}
Город: {}
Машина: {}
Жилье: {}
Основное занятие: {}
Дети: {}
----------------
"""


async def get_unlike_me_profile(my_id, state):  # тут будет выбор ид которые не являются ид юзера
    for i in range(40):  # это короче удалить, записей мало(2) и чтобы оно не кидало мне мою анкету
        r_id = random.choice(lst_of_id)
        if r_id != my_id:
            profile_data = datas.get(r_id)

            await state.update_data(
                current_id_profile=r_id,
                profile=profile_data
            )
            return (r_id, profile_data)

    return


async def send_new_profile(id_, profile_data):
    await bot.send_message(
        id_,
        RESPONCE_TEXT.format(
            profile_data.get("name"),
            profile_data.get("age"),
            profile_data.get("nationality"),
            profile_data.get("education"),
            profile_data.get("town"),
            profile_data.get("car"),
            profile_data.get("own_home"),
            profile_data.get("hobbies"),
            profile_data.get("child")
        ),
        reply_markup=await generate_keyboard(
            profile_data.get("like"),
            profile_data.get("dislike")
        )
    )


@dp.callback_query_handler(text='find_ancets')
async def view_command_handler(call: CallbackQuery, state: FSMContext):
    profile_data = await get_unlike_me_profile(call.from_user.id, state)

    await send_new_profile(call.from_user.id, profile_data[1])


@dp.callback_query_handler()
async def view_query_handler(calldata: types.CallbackQuery,
                             state: FSMContext):  # тут происходит основная работа, выбора анкеты
    if calldata.data == "like":
        profile_state = await state.get_data()  # получение состояния (ид профиля, профиль)
        profile_id = profile_state.get("current_id_profile")  # тут ясно
        profile_info = profile_state.get("profile")

        datas.get(profile_id)["like"] = profile_info.get(
            "like") + 1  # обновляем данные в бд, полсле того как взяли данные из состояния и добавили 1

        await bot.delete_message(calldata.from_user.id, calldata.message.message_id)

        new_profile = await get_unlike_me_profile(calldata.from_user.id, state)
        await send_new_profile(
            calldata.from_user.id,
            new_profile[1]  # короче, после лайка таким же самым способор генерируется новая анкета
        )

    elif calldata.data == "dislike":
        profile_state = await state.get_data()  # получение состояния (ид профиля, профиль)
        profile_id = profile_state.get("current_id_profile")  # тут ясно
        profile_info = profile_state.get("profile")

        datas.get(profile_id)["dislike"] = profile_info.get(
            "dislike") + 1  # обновляем данные в бд, полсле того как взяли данные из состояния и добавили 1

        await bot.delete_message(calldata.from_user.id, calldata.message.message_id)

        new_profile = await get_unlike_me_profile(calldata.from_user.id, state)
        await send_new_profile(
            calldata.from_user.id,
            new_profile[1]  # функия принимает только второй элемент, так как то и есть профиль
        )


    elif calldata.data == "write_to":  # здесь установка состояния для получение сообщения
        await bot.send_message(calldata.from_user.id, "Напишите свое сообщение:")
        await ViewStates.message.set()

    elif calldata.data == "report":  # ты говорил что David уже что-то сделал
        ...


@dp.message_handler(
    state=ViewStates.message)  # обработчик для получения сообщения и отправка по ид который получаем из состояния
async def recv_message_form_profile(message: types.Message, state):
    data_ = await state.get_data()  # получение ид пользователя из состояния

    await bot.send_message(
        data_.get("current_id_profile"),
        f"Сообщение от(<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name} </a>): {message.text}"
    )
    await bot.send_message(message.from_user.id, "Сообщение успешно отправлено")

    await state.finish()