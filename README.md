# DatingBot



## Bot functionality
```/start``` - welcome message with main menu

There are 5 buttons in the main menu\
```Registration```, ```Second menu```, ```Sponsor project```, ```Information```, ```Instruction```

In the second menu you can also see five buttons\
```My profile```, ```Change profile```, ```Preferences```, ```View other profiles```, ```Stop bot```


The main functionality you can find in second menu on button ```View other profile```\
There will be: a photo of the questionnaire, like, dislike, send a message to the user via the bot, complain and leave the viewing of questionnaires, if you stop viewing questionnaires, then you move to the main menu


## Used technology
- Python (tested with 3.8 and 3.9, should work on 3.7+)
- Aiogram
- Docker and Docker Compose
- PostgreSQL

## Preparing for launch
1. Clone this repository via `git clone https://github.com/DavidRomanovizc/DatingBot.git`

2. Setting up a virtual environment\
   `python -m venv venv`
   
3. Activate the virtual environment and set the requirements\
   `pip install -r requirements.txt`
   
4. Rename example environment file `.env.dist` to active environment file`.env` and replace the token with your own

5. Run bot \
   `python app.py`
