<div align="center" height="130px">
  <img src="./media/Logotype.svg" alt="Logotype"/><br/>
  <h1> Doctorinna Telegram bot </h1>
  <p></p>
</div>


> This is the part of the Doctorinna project, check out the [overview repository](https://github.com/Doctorinna/overview) first

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/5e91d2c1d64f41cd9bbfeedb7af7f81c)](https://www.codacy.com/gh/Doctorinna/telegram-bot/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Doctorinna/telegram-bot&amp;utm_campaign=Badge_Grade)

## Table of content
- [About](#about)
- [Getting started](#getting-started)
  - [Techical stack](#tech-stack)
- [Run bot](#run)
  - [Without Docker](#without-docker)
  - [With Docker](#with-docker)
- [Deployment](#deploy)


## 📎 About application <a name="getting-started"></a>
This repository is place for **Doctorinna** Telegram bot - part of the Doctorinna project.
This is an open-source project to determine user's risk groups for several diseases.
It is achieved via questionnaire, people answer a set of questions and get a result on diseases with a piece of advice.
The main building block of the project is its API, I highly recommend visiting its [repository](https://github.com/Doctorinna/backend).

Telegram nowadays is extremely widespread, therefore it was decided to build one of the API frontends using it,
namely with a bot. Please note that the bot does not transfer personal data to the server
(your first name, last name and username are not used at all, only the answers to the questions are processed).

Please feel free to try: [@doctorinna_bot](https://t.me/doctorinna_bot)

## 📌 Getting started <a name="getting-started"></a>

### Technical stack <a name="tech-stack"></a>
First and foremost, the bot is written in **Python** programming language.
It utilizes the fhe [aiogram](https://github.com/aiogram/aiogram) framework and 
uses [Redis](https://redis.io/) as a storage.

### Run locally without Docker <a name="without-docker"></a>

#### Requirements
- In order to launch bot locally, firstly one needs to install the Python interpreter from [the official website](https://www.python.org/downloads/). 
  The version of Python used in this project is **3.9.5**. In order to check that it was installed correctly, type `python --version`.
  The python version should be displayed. Once the interpreter is ready, install all the dependencies by typing in prompt from the project directory:
  ```bash
  pip install -r requirements.txt
  ```

- One also needs to install redis and start redis server. [Here](https://redis.io/download) you can find the official instructions on how to do it. 
  In order to check that it was installed and is running correctly, type `redis-cli ping`. The word PONG should be displayed.
  
#### Start bot
To start the bot, one needs to set up the arguments.
Currently, there are the following arguments needed: `BOT_TOKEN`, `BOT_ADMIN`, `API_URL` `REDIS_IP`, `REDIS_PORT`, `REDIS_DB`.
The latter three have the default values of `localhost`, `6379` and `1` correspondingly, so they can be omitted in this section.

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

   
### Run using Docker <a name="with-docker"></a>
One needs to install `docker-compose` (see the [instructions](https://docs.docker.com/compose/install/)).
Here to run one needs to pass parameters via environment variables,
see an example:
```bash
DOCTORINNA_BOT_TOKEN=0123456789:abcdefghijklmnopqrstuvwxyz012345678 
DOCTORINNA_BOT_ADMIN=123456789 DOCTORINNA_API_URL=https://doctorinna.com/api
docker-compose up
```

## Deployment <a name="deployment"></a>
[Digitalocean](https://www.digitalocean.com/) was used to deploy bot to the server