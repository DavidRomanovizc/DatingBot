# DatingBot

## Used technology 📝

[![Python](https://img.shields.io/badge/Python-3.8%2B-blueviolet?style=flat-square)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-3.1.13-ff69b49cf?style=flat-square)](https://pypi.org/project/aiogram/)
[![Aiogram](https://img.shields.io/badge/aiogram-2.14-9cf?style=flat-square)](https://pypi.org/project/aiogram/)
[![loguru](https://img.shields.io/badge/loguru-0.5-red?style=flat-square)](https://pypi.org/project/aiogram/)
[![asyncpg](https://img.shields.io/badge/asyncpg-0.24-green?style=flat-square)](https://pypi.org/project/aiogram/)

## Bot functionality 🔍️

<br>
Coming soon...
<br>
<br>

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

We try to stick to [PEP 8](https://peps.python.org/pep-0008/#:~:text=Use%20the%20function%20naming%20rules,invoke%20Python's%20name%20mangling%20rules)

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