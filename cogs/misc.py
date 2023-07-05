import asyncio

import disnake
from disnake.ext import commands
from disnake.ext.commands import has_permissions


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
