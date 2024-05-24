# //  TODO transfer settings to this file instead of the settings being all over the place

import datetime
import json
from datetime import datetime as dt

import disnake
import pyrebase
from disnake.ext import commands

embed_color = disnake.Color.dark_red()
embed_error = disnake.Color.red()
embed_warning = disnake.Color.yellow()
embed_success = disnake.Color.green()

guild_members = {}

class Settings(commands.cog):
    def __init__(self, client):
        self.client = client


def setup(client):
    bot.add_cog(Settings(client))
