# DatingBot

## Used technology 📝

[![Python](https://img.shields.io/badge/Python-3.8%2B-blueviolet?style=flat-square)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-3.1.13-ff69b49cf?style=flat-square)](https://pypi.org/project/aiogram/)
[![Aiogram](https://img.shields.io/badge/aiogram-2.14-9cf?style=flat-square)](https://pypi.org/project/aiogram/)
[![loguru](https://img.shields.io/badge/loguru-0.5-red?style=flat-square)](https://pypi.org/project/aiogram/)
[![asyncpg](https://img.shields.io/badge/asyncpg-0.24-green?style=flat-square)](https://pypi.org/project/aiogram/)

## Preparing for launch 🚀

### Environment

| Variable     | Type        | Importance   |
|--------------|-------------|--------------|
| BOT_TOKEN    | str         | True         |
| ADMINS       | list        | True         |
| IP           | str         | True         |
| DB_USER      | str         | True         |
| DB_PASS      | str         | True         |
| DB_HOST      | str         | True         |
| DB_NAME      | str         | True         |

`BOT_TOKEN` - Bot token\
`ADMINS` - list of admins id\
`IP` - ip for other services

`DB_USER` - username of the database owner\
`DB_PASS` - password from the database\
`DB_HOST` - IP address of the database\
`DB_NAME` - database name

### Django 🟢

```shell
python django_app.py makemigrations
python django_app.py migrate
python django_app.py createsuperuser
python django_app.py runserver
```

## Contributing guidelines to action 💡

<hr>

### Code Style Guide

We try to stick
to [PEP 8](https://peps.python.org/pep-0008/#:~:text=Use%20the%20function%20naming%20rules,invoke%20Python's%20name%20mangling%20rules)

### Handlers

1. There must be no buttons in handlers (only in extreme cases, but it is better to put it in a separate file)
2. If we make a handler for buttons, then we use the "text='action'" in the decorator parameters
3. If we are fetching data or updating data, then the function call should be like this: `await db_commands.func(...)`

### Keyboards

1. If you use the "default button", you need to put them in the "keyboard/default" directories.
2. If you are creating a new file, then you should add the prefix "_default" to the filename
3. If you use the "inline button", you need to put them in the "keyboard/inline" directories.
4. If you are creating a new file, then you should add the prefix "_inline" to the filename
5. If you are creating a new keyboard, then you should add the prefix "_keyboard" in the name function

## Project Structure 🔍️

```
📦data
 ┣ 📂locales
 ┃ ┗ 📜init
 ┣ 📜config.py
 ┗ 📜__init__.py
 📦django_project
 ┣ 📂telegrambot
 ┃ ┣ 📂telegrambot
 ┃ ┃ ┣ 📜asgi.py
 ┃ ┃ ┣ 📜settings.py
 ┃ ┃ ┣ 📜urls.py
 ┃ ┃ ┣ 📜wsgi.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂usersmanage
 ┃ ┃ ┣ 📂templates
 ┃ ┃ ┃ ┗ 📂base
 ┃ ┃ ┣ 📜admin.py
 ┃ ┃ ┣ 📜apps.py
 ┃ ┃ ┣ 📜models.py
 ┃ ┃ ┣ 📜tests.py
 ┃ ┃ ┣ 📜views.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📜db.sqlite3
 ┃ ┣ 📜manage.py
 ┃ ┗ 📜__init__.py
 📦filters
 ┣ 📜filters_chat.py
 ┗ 📜__init__.py
 📦handlers
 ┣ 📂channels
 ┃ ┣ 📜__init__.py
 ┣ 📂errors
 ┃ ┣ 📜error_handler.py
 ┃ ┗ 📜__init__.py
 ┣ 📂groups
 ┃ ┣ 📜__init__.py
 ┣ 📂users
 ┃ ┣ 📜admin_handler.py
 ┃ ┣ 📜back_handler.py
 ┃ ┣ 📜change_datas.py
 ┃ ┣ 📜echo_handler.py
 ┃ ┣ 📜filters_handler.py
 ┃ ┣ 📜information.py
 ┃ ┣ 📜premium_handler.py
 ┃ ┣ 📜registration_handler.py
 ┃ ┣ 📜second_menu.py
 ┃ ┣ 📜send_report.py
 ┃ ┣ 📜start_handler.py
 ┃ ┣ 📜statistics.py
 ┃ ┣ 📜support_handler.py
 ┃ ┣ 📜verification_handler.py
 ┃ ┣ 📜view_ques_handler.py
 ┃ ┗ 📜__init__.py
 ┗ 📜__init__.py
 📦keyboards
 ┣ 📂default
 ┃ ┣ 📜get_contact_default.py
 ┃ ┣ 📜get_location_default.py
 ┃ ┗ 📜__init__.py
 ┣ 📂inline
 ┃ ┣ 📜admin_inline.py
 ┃ ┣ 📜back_inline.py
 ┃ ┣ 📜change_data_profile_inline.py
 ┃ ┣ 📜filters_inline.py
 ┃ ┣ 📜guide_inline.py
 ┃ ┣ 📜main_menu_inline.py
 ┃ ┣ 📜menu_profile_inline.py
 ┃ ┣ 📜questionnaires_inline.py
 ┃ ┣ 📜registration_inline.py
 ┃ ┣ 📜report_inline.py
 ┃ ┣ 📜second_menu_inline.py
 ┃ ┣ 📜support_inline.py
 ┃ ┗ 📜__init__.py
 ┗ 📜__init__.py
 📦middlewares
 ┣ 📜agent_support.py
 ┣ 📜language_middleware.py
 ┣ 📜throttling.py
 ┗ 📜__init__.py
 📦states
 ┣ 📜ban_user_states.py
 ┣ 📜find_user.py
 ┣ 📜mailing.py
 ┣ 📜new_data_state.py
 ┣ 📜reg_state.py
 ┣ 📜reports.py
 ┣ 📜view_p.py
 ┗ 📜__init__.py
 📦utils
 ┣ 📂db_api
 ┃ ┣ 📜db_commands.py
 ┃ ┣ 📜postgres.py
 ┃ ┗ 📜__init__.py
 ┣ 📂misc
 ┃ ┣ 📜check_name.py
 ┃ ┣ 📜create_questionnaire.py
 ┃ ┣ 📜ds_name.py
 ┃ ┣ 📜logging.py
 ┃ ┣ 📜throttling.py
 ┃ ┗ 📜__init__.py
 ┣ 📂YandexMap
 ┃ ┣ 📜exceptions.py
 ┃ ┣ 📜test.py
 ┃ ┣ 📜work_with_location.py
 ┃ ┗ 📜__init__.py
 ┣ 📜notify_admins.py
 ┣ 📜set_bot_commands.py
 ┗ 📜__init__.py
 
```