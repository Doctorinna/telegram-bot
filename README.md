# Doctorinna-Telegram bot

This repository is place for Doctorinna Telegram bot - part of the [Doctorinna](https://github.com/Doctorinna) project. 
The bot is built using the [aiogram](https://github.com/aiogram/aiogram) framework. Current version is just a project skeleton.

Later the following are going to be added:
- interaction with API
  - receiving questions and answer options
  - sending user answers
  - receiving questionnaire results
- questionnaire passing
  - handling start message
  - handling user answers
  - displaying the user's result

## Getting started:

### Requirements
The bot is written in Python programming language. In order to launch it locally, one needs to install the interpreter 
from [the official website](https://www.python.org/downloads/). The version of Python used in this project is **3.9.5**.  
In order to check that it was installed correctly, type `python --version`. The python version should be displayed.\
Once the interpreter is ready, install all the dependencies by typing in prompt from the project directory:
```
pip install -r requirements.txt
```

### Environment variables
The next step is to set up the environment variables. For now, there are `BOT_TOKEN` and `ADMIN_IDS` variables.
In order to pass them, one need to rename `.env.example` file into `.env` and fill it in with proper data.  

## Start bot
When the environment is ready, run the bot by typing in prompt from the project directory:
```bash
python bot.py
```