import json
import os
import platform

import disnake
import psutil
import pyrebase
from disnake.ext import commands
from disnake.ext.commands import is_owner

## make cmd dev only

firebase = pyrebase.initialize_app(
    json.load(open("./firebase_config.json", "r")))
db = firebase.database()


class Dev(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def cls(self, ctx):
        try:
            os.system("cls")
            await ctx.send("Cleared the terminal, Daddy.")
        except commands.NotOwner:
            return
        except Exception as e:
            print(f"Error: \nType: {type(e).__name__} \nInfo - {e}")

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
        try:
            try:
                guildid = int(guildinput)
            except:
                await ctx.send("Invalid guild: failed to convert to int")

            try:
                guild = self.client.get_guild(guildid)
            except:
                await ctx.send("Invalid guild")

            try:
                await guild.leave()
                await ctx.send(f"left {guild.name}")
            except:
                await ctx.send("Error leaving")
        except commands.NotOwner:
            return
        except Exception as e:
            print(f"Error: \nType: {type(e).__name__} \nInfo - {e}")

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def servers(self, ctx):
        try:
            await ctx.send(f"{len(self.client.guilds)}")
            listofids = []
            for guild in self.client.guilds:
                listofids.append(guild.id)
            await ctx.send(listofids)
        except commands.NotOwner:
            return
        except Exception as e:
            print(f"Error: \nType: {type(e).__name__} \nInfo - {e}")

def setup(client):
    client.add_cog(Dev(client))
    print(f"Cog: Dev - loaded.")

def teardown(client):
    print(f"Cog: Dev - unloaded.")
