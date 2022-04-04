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
`IP` -  ip for other services

`DB_USER` - username of the database owner\
`DB_PASS` -  password from the database\
`DB_HOST` -  IP address of the database\
`DB_NAME` -  database name

### Django 🟢

```shell
python django_app.py makemigrations
python django_app.py migrate
python django_app.py createsuperuser
python djangp_app.py runserver
```

## Pull requests - a guide to action 💡

If you suddenly write a pull request to any segment of the bot, please leave comments on the key points of your code.
