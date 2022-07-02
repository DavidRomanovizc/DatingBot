# DatingBot

> An open source telegram bot with which you can find new acquaintances

## :books: Table of Contents

- [Installation](#package-installation)
- [Usage](#rocket-usage)
- [Django](#green_book-django)
- [Contributing](#memo-contributing)
- [License](#scroll-license)



## 🖍 Used technology
![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![Postgresql](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)




## :package: Installation

#### First check if you have Python installed

Before installing this DatingBot-project you need to check if you have python\
To check if you have python installed, run this command in your terminal:

```sh
python -V
```

If you get an answer like this, it means that `Python` is installed.

```sh
Python 3.9.5
```

#### Then fork the DatingBot

```sh
https://github.com/DavidRomanovizc/DatingBot.git
```

## :rocket: Usage

First you need to rename the file `.env.dist` to `.env`.\
After that, you need to fill it with data.


| Variable   | Type        | Importance   |
|------------|-------------|--------------|
| BOT_TOKEN  | str         | True         |
| ADMINS     | list        | True         |
| IP         | str         | True         |
| DB_USER    | str         | True         |
| DB_PASS    | str         | True         |
| DB_HOST    | str         | True         |
| DB_NAME    | str         | True         |
| SECRET_KEY | str         | True         |
| API_KEY    | str         | True         |

`BOT_TOKEN` - Bot token\
`ADMINS` - list of admins id\
`IP` - ip for other services

`DB_USER` - username of the database owner\
`DB_PASS` - password from the database\
`DB_HOST` - IP address of the database\
`DB_NAME` - database name

`SECRET_KEY` - secret key for django\
`API_KEY` - yandex api key for yandex map

#### :green_book: Django

Install Django 
```sh
pip install Django
```

To create a `SECRET_KEY` you can use the site to [generate secret keys](https://djecrety.ir/)\
And then paste it into the `.env` file

```sh
SECRET_KEY=jjv@^0qv^=aydunfjo$qpd_66j+)egm1#-c1iwt%mtjinm)ftj
```

Install the jazzmin

```sh
pip install -U django-jazzmin
```

Add jazzmin to your `INSTALLED_APPS` before django.contrib.admin.

```py
INSTALLED_APPS = [
    'jazzmin',

    'django.contrib.admin',
    [...]
]
```

```shell
python django_app.py makemigrations
python django_app.py migrate
python django_app.py createsuperuser
python django_app.py runserver
```

And after that you need to run the file `app.py `

## :memo: Contributing

Before making changes to the project, create a new branch

### Code Style Guide

We try to stick
to [PEP 8](https://peps.python.org/pep-0008/#:~:text=Use%20the%20function%20naming%20rules,invoke%20Python's%20name%20mangling%20rules)

### 1. Handlers

1. There must be no buttons in handlers (only in extreme cases, but it is better to put it in a separate file)
2. If we make a handler for buttons, then we use the "text='action'" in the decorator parameters
3. If we are fetching data or updating data, then the function call should be like this: `await db_commands.func(...)`

### 2. Keyboards

1. If you use the "default button", you need to put them in the "keyboard/default" directories.
2. If you are creating a new file, then you should add the prefix "_default" to the filename
3. If you use the "inline button", you need to put them in the "keyboard/inline" directories.
4. If you are creating a new file, then you should add the prefix "_inline" to the filename
5. If you are creating a new keyboard, then you should add the prefix "_keyboard" in the name function

## :scroll: License

License:\
[MIT License](LICENSE)

![image](https://user-images.githubusercontent.com/72649244/173241368-c40bd408-8df8-450f-9ac7-530de1692e1c.png)

