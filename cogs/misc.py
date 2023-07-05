import asyncio
import os
from io import BytesIO

import disnake
import requests
from disnake.ext import commands
from disnake.ext.commands import has_permissions
from PIL import Image

# //TODO remove unneeded imports and lines of code
# //TODO check for help message is variables are blank

class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content == "80085":
            await message.channel.send("Wow! You found them.")
            await asyncio.sleep(4)
            await message.channel.send("Sadly not in real life...")


def setup(client):
    client.add_cog(Misc(client))
    print(f"Cog: Misc - loaded.")

def teardown(client):
    print(f"Cog: Misc - unloaded.")
