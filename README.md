# DatingBot
 [![Python](https://img.shields.io/badge/Python-3.8%2B-blueviolet?style=flat-square)](https://www.python.org/downloads/)
 [![Django](https://img.shields.io/badge/Django-3.1.13-ff69b49cf?style=flat-square)](https://pypi.org/project/aiogram/)
 [![Aiogram](https://img.shields.io/badge/aiogram-2.14-9cf?style=flat-square)](https://pypi.org/project/aiogram/)
 [![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1.4.21-pink?style=flat-square)](https://pypi.org/project/aiogram/)
 [![loguru](https://img.shields.io/badge/loguru-0.5-red?style=flat-square)](https://pypi.org/project/aiogram/)
 [![asyncpg](https://img.shields.io/badge/asyncpg-0.24-green?style=flat-square)](https://pypi.org/project/aiogram/)
 [![Qiwipy](https://img.shields.io/badge/Qiwipy-2.1.6-important?style=flat-square)](https://pypi.org/project/aiogram/)


## Bot functionality 🔍️
```/start``` - welcome message with main menu

There are 5 buttons in the main menu\
```Registration```, ```Second menu```, ```Sponsor project```, ```Information```, ```Instruction```

In the second menu you can also see five buttons\
```My profile```, ```Change profile```, ```Preferences```, ```View other profiles```, ```Stop bot```


The main functionality you can find in second menu on button ```View other profile```\
There will be: a photo of the questionnaire, like, dislike, send a message to the user via the bot, complain and leave the viewing of questionnaires, if you stop viewing questionnaires, then you move to the main menu


## Used technology 📝
- Python (tested with 3.8 and 3.9, should work on 3.7+)
- Aiogram
- Docker and Docker Compose
- PostgreSQL

## Preparing for launch 🚀
1. Clone this repository via `git clone https://github.com/DavidRomanovizc/DatingBot.git`

2. Setting up a virtual environment\
   `python -m venv venv`
   
3. Activate the virtual environment and set the requirements\
   `pip install -r requirements.txt`
   
4. Rename example environment file `.env.dist` to active environment file`.env` and replace the token with your own

5. Run bot \
   `python app.py`
   
## Pull requests - a guide to action 💡

If you suddenly write a pull request to any segment of the bot, please leave comments on the key points of your code.

In the near future, the bot will be translated into English, and comments will be left everywhere for mutual understanding of the code. ^_^

## Soon...

```Django ORM```
