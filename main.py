import datetime
import json
import os
import sys
import time
import traceback
from datetime import datetime

import disnake
import pyrebase
from decouple import config
from disnake.ext import commands
from disnake.ext.commands import has_permissions, is_owner

# //TODO optimize code so less data is stored in memory and more data is stored locally, would improve speed and efficiency

#import logging
# logging.basicConfig(level=logging.ERROR)
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
    status=disnake.Status.dnd
)
client.remove_command("help")


@client.event
async def on_ready():
    if len(client.guilds) > 1:
        response = "servers"
    else:
        response = "server"
    await client.change_presence(activity=disnake.Activity(type=disnake.ActivityType.watching, name=f"{len(client.guilds)} {response}"), status=disnake.Status.dnd)
    print(
        f"\nLogged in as: {client.user.name} - {client.user.id}\nWrapper Version: {disnake.__version__}\nAt: {datetime.now()}\n"
    )

initial_cogs = [
    "cogs.admin",
    #"cogs.anime",
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
        # print(cog_counter)
    except Exception as e:
        print(f"Error: \nType: {type(e).__name__} \nInfo - {e}")
        print(f"{e}")

if cog_counter >= len(initial_cogs):
    print("All cogs imported succesfully", file=sys.stderr)
    time.sleep(5)
    try:
        os.system("cls")
        os.system("title Royal Knight: STARTED")
    except RuntimeError:
        os.system("clear")
        os.system("Set TERM_TITLE= Royal Knight: STARTED")
else:
    print("\nLoading one or more cogs failed...\n")
    time.sleep(5)
    try:
        os.system("cls")
        os.system("title Royal Knight: ERROR IN A COG")
    except RuntimeError:
        os.system("clear")
        os.system("Set TERM_TITLE= Royal Knight: ERROR IN A COG")


client.run(config("token"), reconnect=True)