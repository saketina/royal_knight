import asyncio
import datetime
import os
from datetime import datetime, date
from io import BytesIO

import disnake
from disnake.ext import commands
from disnake.ext.commands import guild_only
from PIL import Image

import logging

logging = logging.getLogger("User")

class User(commands.Cog):

	def __init__(self, client):
		self.client=client

	# TODO PROFILE/add badges
	# TODO PROFILE/add total messages, most used channel, etc...
	@commands.command(pass_context=True)
	@commands.guild_only()
	async def profile(self, ctx, user: disnake.Member = None):
		await ctx.trigger_typing()
		if not user:
			user = ctx.author
		#logging.info(user.raw_status)
		if user.raw_status == "online":
			status_pic = "cogs/Assets/member_status/online.png"
		elif user.raw_status == "idle":
			status_pic = "cogs/Assets/member_status/idle.png"
		elif user.raw_status == "dnd":
			status_pic = "cogs/Assets/member_status/dnd.png"
		elif user.raw_status == "offline":
			status_pic = "cogs/Assets/member_status/offline.png"
		else:
			status_pic = "cogs/Assets/member_status/error.png"

		
		file = disnake.File(status_pic, filename="status.png")

		ProfileEmbed = disnake.Embed(
		  color=disnake.Color.dark_red(),
		  timestamp=datetime.now()
		  )
		ProfileEmbed.set_author(name=user.display_name, icon_url= "attachment://status.png")
		ProfileEmbed.set_thumbnail(url = user.display_avatar)
		char_count = 0
		char_overload = False

		#roleList = [r.mention & char_count += len(r.mention) for r in user.roles if r != ctx.guild.default_role]
		roleList = []
		TempList = []
  
		for r in user.roles:
			if r != ctx.guild.default_role:
				TempList.append(r.mention)
		TempList.reverse()
		for i in TempList:
			if char_count <= 800:
				roleList.append(i)
				char_count += len(r.mention)
			else:
				char_overload = True
				
		if char_overload == True:
			roleList.append("**`and a lot more...`**")
		else:
			pass

		if roleList != []:
			rolesAddon = "> " + '\n > '.join(roleList)
		else:
			rolesAddon = "None"

		ProfileEmbed.add_field(
		name=f"Roles ({len(roleList)})",
		value=rolesAddon,
		inline=False
		)
		
		joined_at = user.joined_at.strftime("%b %d, %Y, %T")
		
		days_join = datetime.now() - user.joined_at.replace(tzinfo=None)
		
		ProfileEmbed.add_field(
		name="Joined at",
		value=f"{joined_at} ({days_join.days} day\'s ago)",
		inline=True
		)
		
		created_at = user.created_at.strftime("%b %d, %Y, %T")
		
		days_created = datetime.now() - user.created_at.replace(tzinfo=None)
		
		ProfileEmbed.add_field(
		name="Created at",
		value=f"{created_at} ({days_created.days} day\'s ago)",
		inline=False
		)

		if user.is_on_mobile() == True:
			device = "mobile"
		else:
			device = "PC"
			
		if user.bot == True:
			user_bot = "🤖"
		elif user.system == True:
			user_bot = "**Discord staff**"
		else:
			user_bot = "😎"
		
		if ctx.guild.get_role(698297658137116793) in user.roles:
			booster = "Yes\n"
		else:
			booster = "No\n"

		if user.premium_since == None:
			premium_time = "Not boosting"
		else:
			premium_time = user.premium_since
		
		if booster == "Yes":
			boosting_since = f"Boosting since: ()\n".format(premium_time.strftime("%d %B %Y"))
		else:
			boosting_since = ""
			
		if user.voice == None:
			voice_state = ""
		else:
			user_voice = user.voice
			voice_state = f"In voice channel: <#{user_voice.channel.id}>"
			
		ProfileEmbed.add_field(
			name="General info",
			value=f"Device: {device}\n"
				  f"Type: {user_bot}\n"
				  f"Booster: {booster}{boosting_since}{voice_state}",
			inline=True
		)
		ProfileEmbed.set_footer(
		text="User ID: " + str(user.id),
		icon_url = user.role_icon
		)
		
		await ctx.send(embed = ProfileEmbed, file=file)

	@commands.command(aliases=["av", "avatar"], pass_context=True)
	async def pfp(self, ctx, member: disnake.Member = None):
		if member is None:
			member = ctx.author

		avatar_url = member.display_avatar
		avatar_embed = disnake.Embed(
			title=f"{member}'s Avatar",
			color=disnake.Color.dark_red()
		)
		avatar_embed.set_image(url=avatar_url)

		await ctx.send(embed=avatar_embed)

def setup(client):
	client.add_cog(User(client))

