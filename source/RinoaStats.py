import disnake
import disnake.ext.commands as commands

import json
import logging

# Logging-Config
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%d.%m.%Y %H:%M:%S',
    handlers=[logging.StreamHandler(), logging.FileHandler('bot.log')]
)

intents = disnake.Intents.all()
intents.reactions = True
bot = commands.Bot(
    command_prefix=Rinoa,
    intents=intents,
    help_command=None,
)

# loads the config file located  in source
with open('config.json', 'r') as file:
    config = json.load(file)


# loads the events that are in the source.event.on folder
bot.load_extension("event.on.on_ready")
bot.load_extension("event.updatestats")
bot.load_extension("event.syncstats")


def main():
    bot.run(config["bot"]["Token"])

main()