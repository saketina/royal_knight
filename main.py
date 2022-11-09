import os
try:
    import disnake
except ImportError:
    os.system("pip install -U disnake[voice]")
    os.system("pip install -U aiofiles")
    os.system("pip install -U pillow")
    os.system("pip install -U python-decouple")
    os.system("pip install -U requests")
    os.system("pip install -U pyrebase4")

from disnake.ext import commands
from disnake.ext.commands import is_owner

import traceback
import sys
import json
import pyrebase
import time

#import logging
#logging.basicConfig(level=logging.ERROR)
cog_counter = 0

intents = disnake.Intents.all()
intents.members = True
intents.guilds = True
intents.message_content = True
intents.messages = True

def get_prefix(client, message):
    prefixes = ["k.", "K.", "<@850019720648589352>"]
    return commands.when_mentioned_or(*prefixes)(client, message)

client = commands.Bot(
    command_prefix = get_prefix,
    case_insensitive=True,
    intents=intents,
    reload=True,
    status = disnake.Status.dnd
    )
client.remove_command("help")

@client.event
async def on_ready():
    if len(client.guilds) > 1:
        response = "servers"
    else:
        response = "server"
    await client.change_presence(activity = disnake.Activity(type=disnake.ActivityType.watching, name=f"{len(client.guilds)} {response}"), status = disnake.Status.dnd)
    print(
        f"\nLogged in as: {client.user.name} - {client.user.id}\nWrapper Version: {disnake.__version__}\n"
        )

@client.command(pass_context=True)
@is_owner()
async def load(ctx, cog):
    try:
        client.load_extension(f"cogs.{cog}")
        await ctx.send(f"Cog: **{cog}** has been loaded!")
    except commands.ExtensionAlreadyLoaded:
        await ctx.send(f"Error: **{cog}** is already loaded.")
    except Exception as e:
        print(f"Error: \nType: {type(e).__name__} \nInfo - {e}")

@load.error
async def load_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Error: Please enter a cog.")

@client.command(pass_context=True)
@is_owner()
async def unload(ctx, cog):
    try:
        client.unload_extension(f"cogs.{cog}")
        await ctx.send(f"Cog: **{cog}** has been unloaded!")
    except commands.ExtensionNotLoaded:
        await ctx.send(f"Error: **{cog}** is not loaded.")
    except Exception as e:
        print(f"Error: \nType: {type(e).__name__} \nInfo - {e}")

@unload.error
async def unload_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a cog.")

@client.command(pass_context=True)
@is_owner()
async def reload(ctx, cog):
    try:
        client.reload_extension(f"cogs.{cog}")
        await ctx.send(f"Cog: **{cog}** has been reloaded!")
    except commands.ExtensionNotLoaded:
        await ctx.send(f"Error: **{cog}** is not loaded.")
    except Exception as e:
        print(f"Error: \nType: {type(e).__name__} \nInfo - {e}")

@reload.error
async def reload_error(ctx, error):
    try:
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter a cog.")
    except commands.ExtensionNotLoaded:
        await ctx.send(f"Cog: **{cog}** has not been loaded.")
    except Exception as e:
        print(f"Error: \nType: {type(e).__name__} \nInfo - {e}")

initial_cogs = [
    "cogs.anime",
    "cogs.counters",
    "cogs.fun",
    "cogs.help",
    "cogs.misc",
    "cogs.moderation",
    "cogs.prefix",
    "cogs.roleplay",
    "cogs.user",
    "cogs.utility",
    "cogs.welcome"
]

for cog in initial_cogs:
    try:
        client.load_extension(cog)
        cog_counter += 1
        #print(cog_counter)
    except Exception as e:
        #print(f"Error: \nType: {type(e).__name__} \nInfo - {e}")
        print(f"{e}")

if cog_counter >= 11:
    print("\nAll cogs imported succesfully")
    time.sleep(5)
    try:
        os.system("cls")
    except:
        os.system("clear")
    os.system("title Karma Bot: STARTED")
else:
    print("\nLoading one or more cogs failed...\n")
    time.sleep(5)
    try:
        os.system("cls")
    except:
        os.system("clear")
    os.system("title Karma Bot: ERROR IN A COG")

client.run("ODUwMDE5NzIwNjQ4NTg5MzUy.YLjojg.tMwU324N8DBF1yMfMWOwQdw5axE", reconnect = True)