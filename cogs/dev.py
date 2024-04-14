import json
import os
import platform

import disnake
import psutil
import pyrebase
from disnake.ext import commands
from disnake.ext.commands import is_owner

import logging

logging = logging.getLogger("Dev")

firebase = pyrebase.initialize_app(
    json.load(open("./firebase_config.json", "r")))
db = firebase.database()


class Dev(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def cls(self, ctx):
        os.system("cls")
        await ctx.send("Cleared the terminal, Daddy.")

    @commands.command()
    @commands.is_owner()
    async def system_info(self, ctx):
        # Get system information
        system_info = {
            "Operating System": platform.system(),
            "Release Version": platform.release(),
            "CPU Usage": f"{psutil.cpu_percent()}%",
            "RAM Usage": f"{psutil.virtual_memory().percent}%",
            "Disk Usage": f"{psutil.disk_usage('/').percent}%",
        }

        # Create an embed to display the information
        embed = disnake.Embed(title="System Information", color=disnake.Color.blue())

        for key, value in system_info.items():
            embed.add_field(name=key, value=value, inline=False)

        await ctx.send(embed=embed)    

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def leave(self, ctx, *, guildinput):
        guildid = int(guildinput)
        guild = self.client.get_guild(guildid)
        await guild.leave()

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def servers(self, ctx):
        await ctx.send(f"{len(self.client.guilds)}")
        listofids = []
        for guild in self.client.guilds:
            listofids.append(guild.id)
        await ctx.send(listofids)

def setup(client):
    client.add_cog(Dev(client))
    print(f"Cog: Dev - loaded.")

def teardown(client):
    print(f"Cog: Dev - unloaded.")
