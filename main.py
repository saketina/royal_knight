import json
import os
import sys
import time
import traceback
import datetime
from datetime import datetime as dt

import subprocess

import disnake
import pyrebase
from decouple import config
from disnake.ext import commands
from disnake.ext.commands import has_permissions, is_owner

import logging

#?# TODO optimize code so less data is stored in memory and more data is stored locally, would improve speed and efficiency

start_time = time.time()

try:
    os.mkdir("logs")
except:
    pass

log_file_path = 'logs/client.log'
os.system("ls")

"""logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=log_file_path,
                    filemode='w')
"""
logger = logging.getLogger('disnake')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(filename=log_file_path, encoding='utf-8', mode='w')
file_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
terminal_handler = logging.StreamHandler()
file_handler.setFormatter(logging.Formatter('%(levelname)s:%(name)-15s: %(message)s'))
logger.addHandler(file_handler)
logger.addHandler(terminal_handler)

cog_counter = 0

intents = disnake.Intents.all()
intents.presences=False

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
        f"\nLogged in as: {client.user.name} - {client.user.id}\nWrapper Version: {disnake.__version__}\nAt: {dt.now()}\n"
    )
    pass

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
        description="Updated the current host server",
        color=disnake.Color.dark_red()
    )
    os.system("git pull")
    await ctx.send(embed=embed)
    
@client.command()
async def info(ctx):
    embed = disnake.Embed(
        title="General Information",
        color=disnake.Color.dark_red(),
        timestamp=dt.now()
    )
    current_time = time.time()
    difference = int(round(current_time - start_time))
    text = str(datetime.timedelta(seconds=difference))
    embed.add_field(
        name="Bot info",
        value=f"Uptime: {text}\n"
                f"Shard ID: {ctx.guild.shard_id}\n"
                #f"Currently serving {len(self.client.guilds)} servers"
    )
    embed.add_field(
        name="Developer",
        value=f"Discord: thecrazydragon({client.owner.mention})"
    )
    #embed.set_thumbnail(client.owner.avatar)
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
