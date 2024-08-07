import datetime
import json
import os
import sys
import time
import traceback
from datetime import datetime

import subprocess

import disnake
import pyrebase
from decouple import config
from disnake.ext import commands
from disnake.ext.commands import has_permissions, is_owner

import logging

# //TODO optimize code so less data is stored in memory and more data is stored locally, would improve speed and efficiency


if os.name == "nt":
    log_file_path = 'logs/client.log'
elif os.name == "posix" :
    log_file_path = '~/logs/client.log'
else:
    log_file_path = 'logs/client.log'
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=log_file_path,
                    filemode='w')

logger = logging.StreamHandler()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)s: %(levelname)s: %(message)s')
logger.setFormatter(formatter)
logging.getLogger('').addHandler(logger)

cog_counter = 0

intents = disnake.Intents.all()

def get_prefix(client, message):
    prefixes = ["k.", "K.", "<@850019720648589352>"]
    return commands.when_mentioned_or(*prefixes)(client, message)


client = commands.Bot(
    command_prefix=get_prefix,
    case_insensitive=True,
    intents=intents,
    reload=True,
    status=disnake.Status.dnd,
    strip_after_prefix=True,
    chunk_guilds_at_startup=False,
    shard_count=1,
    shard_id=0
)
client.remove_command("help")

@client.event
async def on_ready():
    logging.info(
        f"\nLogged in as: {client.user.name} - {client.user.id}\nWrapper Version: {disnake.__version__}\nAt: {datetime.now()}\n"
    )

@client.command()
@is_owner()
async def restart(ctx):
    embed = disnake.Embed(
        title = ":white_check_mark:",
        description = "Restarted my system",
        color = disnake.Color.dark_red()
        )
    await ctx.send(embed = embed)
    os.system("clear")
    os.execv(sys.executable, ["python"] + sys.argv)
    #await ctx.send("restarted the bot, boss.")
    
@client.command()
@is_owner()
async def update(ctx):
    embed = disnake.Embed(
        title="Updated the current host server",
        color=disnake.Color.dark_red()
    )
    os.system("git pull")
    await ctx.send(embed=embed)

initial_cogs = [
    "cogs.admin",
    #"cogs.anime",
    #"cogs.cache",
    #"cogs.counters",
    "cogs.fun",
    "cogs.gah",
    "cogs.help",
    "cogs.misc",
    "cogs.moderation",
    "cogs.prefix",
    "cogs.roleplay",
    "cogs.testing",
    "cogs.user",
    "cogs.utility",
    #"cogs.welcome"
]

for cog in initial_cogs:
    try:
        client.load_extension(cog)
        cog_counter += 1
        logging.info(f"Loaded {cog}")
    except Exception as e:
        logging.error(f"Failed to load {cog}, {e}")

if cog_counter >= len(initial_cogs):
    logging.info("All cogs imported succesfully")
else:
    logging.warning("\nLoading one or more cogs failed...\n")

client.run(config("token"), reconnect=True)
