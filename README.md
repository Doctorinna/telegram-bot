# Doctorinna-Telegram bot

This repository is place for Doctorinna Telegram bot - part of the [Doctorinna](https://github.com/Doctorinna) project. 
The bot is built using the [aiogram](https://github.com/aiogram/aiogram) framework.

Later the following are going to be added:
  - interaction with API
    - receiving questions and answer options
    - sending user answers
    - receiving questionnaire results
  - questionnaire passing
    - handling start message
    - handling user answers
    - displaying the user's result

## Getting started

### Run locally without Docker

#### Requirements
  - **Python**:  
    In order to launch it locally, one needs to install the interpreter from [the official website](https://www.python.org/downloads/).
    The version of Python used in this project is **3.9.5**. In order to check that it was installed correctly, type `python --version`.
    The python version should be displayed. Once the interpreter is ready, install all the dependencies by typing in prompt from the project directory:
    ```bash
    pip install -r requirements.txt
    ```

  - **Redis**:  
    One also needs to install redis and start redis server. [Here](https://redis.io/download) you can find the official instructions on how to do it.
    In order to check that it was installed and is running correctly, type `redis-cli ping`. The word PONG should be displayed.
  
#### Start bot
To run the bot, one need to set up the arguments.
Currently, there are the following arguments needed: `BOT_TOKEN`, `BOT_ADMIN`, `API_URL` `REDIS_IP`, `REDIS_PORT`, `REDIS_DB`.
The latter three have the default values of `localhost`, `6379` and `1` correspondingly, so you can omit them.

To get the description on arguments passing, one can type `python -m bot --help`, yet I will explain it further.

There are several ways how to pass these arguments:

  1) Through the command line  
     Example:  
     ```bash
     python -m bot --bot-token 0123456789:abcdefghijklmnopqrstuvwxyz012345678 --bot-admin 123456789 --api-url https://doctorinna.com/api
     ```
     

  2) Via config file  
     Create `config.yml` file in the project directory and fill it with data (refer to `config-example.yml` for the example).
     To run, execute the following command: `python -m bot`.

   
### Run using Docker
Firstly, one needs to install `docker-compose` (see the [instructions](https://docs.docker.com/compose/install/)).
Then, create `docker-compose.yml` file, copy contents of `docker-compose-example.yml`, provide proper environment variables in it
(note that the variables should be prefixed with DOCTORINNA_) and run:
```bash
docker-compose up
```