import asyncio
import datetime
import os
from datetime import datetime
from io import BytesIO

import disnake
from disnake.ext import commands
from disnake.ext.commands import guild_only
from PIL import Image

class User(commands.Cog):

    def __init__(self, client):
        self.client=client

    # //TODO PROFILE/add badges
    # //TODO PROFILE/add if Member is a booster or has nitro
    # //TODO PROFILE/add checks if member is on mobile or on pc
    @commands.command(pass_context=True)
    @commands.guild_only()
    async def profile(self, ctx, user: disnake.Member = None):

        if not user:
            user = ctx.author
        #print(user.raw_status)
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

        roleList = [r.mention for r in user.roles if r != ctx.guild.default_role]
        roleList.reverse()

        if roleList != []:
            rolesAddon = "> " + '\n > '.join(roleList)
        else:
            rolesAddon = "None"

        ProfileEmbed.add_field(
        name="Roles",
        value=rolesAddon,
        inline=False
        )
        joined_at = user.joined_at.strftime("%b %d, %Y, %T")
        ProfileEmbed.add_field(
        name="Joined at",
        value=f"{joined_at}",
        inline=False
        )
        created_at = user.created_at.strftime("%b %d, %Y, %T")
        ProfileEmbed.add_field(
        name="Created at",
        value=f"{created_at}",
        inline=False
        )
        ProfileEmbed.set_footer(
        text="User ID: " + str(user.id)
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
    print("Cog: User - loaded.")

def teardown(client):
    print("Cog: User - unloaded.")
