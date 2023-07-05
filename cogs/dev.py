import asyncio
import json
import time
import typing

import aiofiles
import disnake
import pyrebase
from disnake.ext import commands, tasks
from disnake.ext.commands import guild_only, is_owner

firebase = pyrebase.initialize_app(
    json.load(open("firebase_config.json", "r")))
db = firebase.database()


class Utility(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command(name='eval', pass_context=True)
    @commands.is_owner()
    async def eval_command(self, ctx, *, expr):
        try:
            if 'await ' in expr:
                new_expr = expr.replace('await ', '')
                ans = await eval(new_expr)
            else:
                ans = eval(expr)
            await ctx.send(f"Answer: {ans}")
        except Exception as e:
            print(e.__traceback__)
            await ctx.send("Didn't work.")

    @commands.command(name="toggle", pass_context=True)
    @commands.is_owner()
    async def toggle(self, ctx, *, command):
        command = self.client.get_command(command)

        if command is None:
            embed = disnake.Embed(title="ERROR", description="I can't find a command with that name!", color=0xff0000)
            await ctx.send(embed=embed)

        elif ctx.command == command:
            embed = disnake.Embed(title="ERROR", description="You cannot disable this command.", color=0xff0000)
            await ctx.send(embed=embed)

        else:
            command.enabled = not command.enabled
            ternary = "enabled" if command.enabled else "disabled"
            embed = disnake.Embed(title="Toggle", description=f"I have {ternary} {command.qualified_name} for you!", color=0xff00c8)
            await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def leave(self, ctx, *, guildinput):
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
