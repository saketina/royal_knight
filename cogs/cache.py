import datetime
import json
from datetime import datetime as dt
import traceback

import disnake
import pyrebase
from disnake.ext import commands

guild_members = None

class Cache(commands.Cog):
	def __init__(self, client):
		self.client = client

	#@commands.Cog.listener()
	#async def on_command_error(self, ctx, error):
	#    await ctx.send(error)

	@commands.command()
	async def fill_cache(self, ctx):
		for guild in self.client.guilds:
			for member in guild.members:
				if guild_members == None:
					guild_members = {guild.id:member}
				else:
					data = {guild.id:member}
					guild_members[guild.id] = data

			print(guild_members[guild.id])

			print(f'guild {guild.name} added to cache')
		await ctx.send("cache has been filled")
		
	@commands.command()
	async def flush_cache(self, ctx):
		for guild in self.client.guilds:
			guild_members[guild.id] = {}
			print(f'guild {guild.name} removed from cache')
		await ctx.send("cache has been flushed")
		
	@commands.command()
	async def print_cache(self, ctx):
		await ctx.send(guild_members[ctx.guild.id])

	@commands.command()
	async def test(self, ctx, user):
		member_list = guild_members[ctx.guild.id]
		print(member_list[user])
		#await ctx.send(member[user])

def setup(client):
	client.add_cog(Cache(client))
	print(f"Cog: Cache - loaded.")

def teardown(client):
	print(f"Cog: Cache - unloaded.")