<h1 align="center">
  Discord.py bot template
</h1>

<h3 align="center">
    A discord bot template to speed up your awesome bot development!
</h3>

<p align="center">

<a href="https://github.com/janaSunrise/discordpy-bot-template">
    <img src="https://img.shields.io/github/languages/code-size/janaSunrise/discordpy-bot-template" alt="Code Size" />
</a>

<a href="https://discord.gg/cSC5ZZwYGQ">
    <img src="https://discordapp.com/api/guilds/695008516590534758/widget.png?style=shield" alt="Discord" />
</a>

</p>

<h3 align="center">
  <a href="https://github.com/janaSunrise/discordpy-bot-template/issues">Report a bug</a>
  <span> · </span>
  <a href="https://discord.gg/cSC5ZZwYGQ">Discord</a>
</h3>

## Requirements

- Python [3.7 or above] - https://www.python.org/downloads/
- Git - https://git-scm.com/download/
- Pipenv [Python package] - Install it using `pip install pipenv`

## Project and code structure information

- Autoloader: The project comes with an autoloader for cogs, that finds all the 
directories / files which have a `setup` attribute and loads them. You can have a `__init__.py`
to load all of them, as the core cog, or have a file with a setup function.

- `core/` Directory is preserved for keeping important things for your bot, such as
converters, decorators and other tools which are really necessary.

- `config.py` contains the configuration and attributes for the bot to use to run and display 
in commands.

- `__main__.py` is present for initializing and running the bot.

- `__init__.py` contains the subclass of the bot with custom features

- The bot comes with a customized error handler, help command, and owners only command.

- There is logging setup all over the bot, which you can also use too when developing it.
You need to import the logger, `from loguru import logger` and just start logging without hassle!

- Global session: Sometimes you need to use `aiohttp` for fetching from the web, and people usually
forget closing it. I added a global session that can be used anywhere using the `self.bot.session` attribute
and it's opening and closing is handled in the subclass.

- Docker information: There is docker compose for multiple containers and services, like postgres, lavalink and 
more. If you need help you can contact. There is also a script for waiting for services that makes life easier too.
Customize it according to the services you use, and the waiting needed for it.

## Creating the bot on Discord

1. Create bot on Discord's [bot portal](https://discord.com/developers/applications/)
2. Make a **New Application**
3. Go to **Bot** settings and click on **Add Bot**
4. Give **Administrator** permission to bot
5. You will find your bot **TOKEN** there, it is important that you save it
6. Go to **OAuth2** and click bot, than add **Administrator** permissions
7. You can follow the link that will appear to add the bot to your discord server

## Installation

This is a guide to help you self host the Bot, and use it privately which simplifies the work, and allows you to have
a bot for yourself and developed it further.

## Docker

**NOTE**: The docker is being tested and being made to worked properly. It hasn't been working perfectly yet. I advise
to use non docker steps until the docker works perfectly when deploying / running. Sorry for this inconvenience.

Docker is an easy way of containerizing and delivering your applications quickly and easily, in an 
convenient way. It's really simple to get started with this, with docker handling all the installation
and other tasks.Configure the environmental variables by renaming the `.env.example` file to `.env` with the respective 
values. Then, run `docker-compose --env-file .env up` after getting the project and config ready.

**Docker mini guide:**

- Running the bot: `docker-compose up --build`
- Stopping the bot: `docker-compose down`
- Rebuilding the bot: `docker-compose build`

### Self hosting without docker

This is a clean and neat way of hosting without using docker. You can follow this if docker doesn't work
well on your system, or it doesn't support it. Containers are resource intensive, and your PC might not
be able to do it, this is the perfect method to get started with the self-hosting.

- Clone or fork the repository, whichever suits you better.
- Install `pipenv`, a virtual env for python. Command: **`pip install pipenv`**
- Create the virtual environment and prepare it for usage using `pipenv update`
- Configure the environmental variables by renaming the `.env.example` file to `.env` with the respective 
  values for it. If you're using heroku or other platforms that have option for external environmental
  variables, use that instead of `.env`
- Configure the options and settings available in `config.py` inside the Bot module, according to your
  preferences.
- Run the server using `pipenv run start`

## 💬 Get in touch

If you have various suggestions, questions or want to discuss things with our community, Have a look at
[Github discussions](https://github.com/janaSunrise/discordpy-bot-template/discussions) or join our discord server!

[![Discord](https://discordapp.com/api/guilds/695008516590534758/widget.png?style=shield)](https://discord.gg/cSC5ZZwYGQ)

## 🙌 Show your support

Be sure to leave a ⭐️ if you like the project!

## ▶ Links
- [Official Documentation](https://discordpy.readthedocs.io/en/latest/)
- [Raise an Issue](https://github.com/janaSunrise/discordpy-bot-template/issues)

## License

This project uses GPL v3. Please be sure to follow the rules and the license. For more info, check [here](https://www.gnu.org/licenses/gpl-3.0.en.html)

<p align="center">

Made by janaSunrise with ❤

</p>


