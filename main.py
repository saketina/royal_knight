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

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='logs/client.log',
                    filemode='w')

console = logging.StreamHandler()
console.setLevel(logging.WARNING)
formatter = logging.Formatter('%(name)s: %(levelname)s: %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

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
    logging.warning(
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
        subprocess.run(["clear"], check=True)
        #subprocess.run(["cls", "title Royal Knight: STARTED"])
    except:
        os.system("cls")
        os.system("title Royal Knight: STARTED")
        
else:
    print("\nLoading one or more cogs failed...\n")
    time.sleep(5)
    try:
        #subprocess.run(["cls", "title Royal Knight: STARTED"], check=True)
        subprocess.run(["cls"], check=True)
    except:
        os.system("cls")
        os.system("title Royal Knight: ERROR IN A COG")

client.run(config("token"), reconnect=True)
