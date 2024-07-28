# //  TODO transfer settings to this file instead of the settings being all over the place

import datetime
import json
from datetime import datetime as dt
from typing import Optional
from colour import Color

import disnake
import pyrebase
from disnake.ext import commands

embed_color = disnake.Color.dark_red()
default_embed_color = disnake.Color.dark_red()
embed_error = disnake.Color.red()
embed_warning = disnake.Color.yellow()
embed_success = disnake.Color.green()

guild_members = {}

def check_color(color):
    try:
        # Converting 'deep sky blue' to 'deepskyblue'
        color = color.replace(" ", "")
        Color(color)
        # if everything goes fine then return True
        return True
    except ValueError: # The color code was not found
        return False

class Settings(commands.cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def color(self, ctx, option=["set", "default"], new_color: Optional[None] = None):
        if check_color(new_color) == True:
            if option == "set":
                await ctx.send("set")
        else:
            await ctx.send("Incorrect input!\nPlease give me a valid color")

def setup(client):
    client.add_cog(Settings(client))
