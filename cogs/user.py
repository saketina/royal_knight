import asyncio
import datetime
import os
from datetime import datetime
from io import BytesIO

import disnake
import requests
from disnake.ext import commands
from disnake.ext.commands import guild_only
from PIL import Image

# //TODO add badges to profile command
# //TODO add if Member is a booster or has nitro

class User(commands.Cog):

    def __init__(self, client):
        self.client=client


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

    @commands.command(name="pfp", aliases=["av", "avatar"], pass_context=True)
    async def pfp(self, ctx, user: disnake.Member = None):

        if not user:
            user = ctx.author

        members = ctx.message.mentions
        if members == []:
            members = [ctx.author]
        imgs = []

        for mem in members:
            url = requests.get(mem.display_avatar)
            im = Image.open(BytesIO(url.content)).resize((500, 500))
            imgs.append(im)
        s = len(imgs)
        bg = Image.new(mode="RGBA", size=(500*s, 500))
        i = 0
        for x in range(0, s):
            try:
                bg.paste(imgs[i], (500*x, 0))
                i += 1
            except Exception as e:
                print(e, i)
                pass
        bg.save(f'images/generated/{ctx.author.id}.png', quality=10)
        file = disnake.File(f"images/generated/{ctx.author.id}.png", filename='pic.jpg')
        emb = disnake.Embed(
            title=f"{user.display_name}\'s avatar",
            description=f"",
            color=disnake.Color.dark_red()
            )
        emb.set_image(url="attachment://pic.jpg")
        await ctx.send(file=file, embed=emb)
        # await ctx.send(file=file)
        try:
            os.system(f"del /Q \"C:/Users/User/Documents/Discord Projects/karma-master/images/generated/{ctx.author.id}.png\"")
        except:
            os.system(f"rm -rf  images/generated/{ctx.author.id}.png")

def setup(client):
    client.add_cog(User(client))
    print("Cog: User - loaded.")

def teardown(client):
    print("Cog: User - unloaded.")
