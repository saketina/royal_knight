import json
import os
from random import choice

import disnake
import pyrebase
from disnake.ext import commands

# //TODO ALL/make counter for times used on someone and times used by someone
# //TODO ALL/make different gifs displayed if ctx.author used the command on themselves

firebase = pyrebase.initialize_app(json.load(open("firebase_config.json", "r")))
db = firebase.database()

class Roleplay(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def bite(self, ctx, member:disnake.Member=None):
        if member is None or member == ctx.author:
            target = "themselves"
        else:
            target = member.mention

        gifs = os.listdir(f"./RP/bite/")
        if gifs == []:
            return

        rnd_gif = choice(gifs)
        path_to_gif = f"./RP/bite/{rnd_gif}"
        file = disnake.File(path_to_gif, filename="gif.gif")

        kiss_embed = disnake.Embed(
            title="",
            description=f"{ctx.author.mention} bit {target}",
        )
        kiss_embed.set_image(url="attachment://gif.gif")

        await ctx.send(embed=kiss_embed, file=file)

    @commands.command(pass_context=True)
    async def blush(self, ctx, member:disnake.Member=None):
        if member is None or member == ctx.author:
            target = "themselves"
        else:
            target = member.mention

        gifs = os.listdir(f"./RP/blush/")
        if gifs == []:
            return

        rnd_gif = choice(gifs)
        path_to_gif = f"./RP/blush/{rnd_gif}"
        file = disnake.File(path_to_gif, filename="gif.gif")

        kiss_embed = disnake.Embed(
            title="",
            description=f"{ctx.author.mention} blushed at {target}",
        )
        kiss_embed.set_image(url="attachment://gif.gif")

        await ctx.send(embed=kiss_embed, file=file)

    @commands.command(pass_context=True)
    async def bonk(self, ctx, member:disnake.Member=None):
        if member is None or member == ctx.author:
            target = "themselves"
        else:
            target = member.mention

        gifs = os.listdir(f"./RP/bonk/")
        if gifs == []:
            return

        rnd_gif = choice(gifs)
        path_to_gif = f"./RP/bonk/{rnd_gif}"
        file = disnake.File(path_to_gif, filename="gif.gif")

        kiss_embed = disnake.Embed(
            title="",
            description=f"{ctx.author.mention} bonked {target}",
        )
        kiss_embed.set_image(url="attachment://gif.gif")

        await ctx.send(embed=kiss_embed, file=file)

    @commands.command(pass_context=True)
    async def boop(self, ctx, member:disnake.Member=None):
        if member is None or member == ctx.author:
            target = "themselves"
        else:
            target = member.mention

        gifs = os.listdir(f"./RP/boop/")
        if gifs == []:
            return

        rnd_gif = choice(gifs)
        path_to_gif = f"./RP/boop/{rnd_gif}"
        file = disnake.File(path_to_gif, filename="gif.gif")

        kiss_embed = disnake.Embed(
            title="",
            description=f"{ctx.author.mention} booped {target}",
        )
        kiss_embed.set_image(url="attachment://gif.gif")

        await ctx.send(embed=kiss_embed, file=file)

    @commands.command(pass_context=True)
    async def cry(self, ctx, member:disnake.Member=None):
        if member is None or member == ctx.author:
            target = "themselves"
        else:
            target = member.mention

        gifs = os.listdir(f"./RP/cry/")
        if gifs == []:
            return

        rnd_gif = choice(gifs)
        path_to_gif = f"./RP/cry/{rnd_gif}"
        file = disnake.File(path_to_gif, filename="gif.gif")

        kiss_embed = disnake.Embed(
            title="",
            description=f"{ctx.author.mention} cried at {target}",
        )
        kiss_embed.set_image(url="attachment://gif.gif")

        await ctx.send(embed=kiss_embed, file=file)

    @commands.command(pass_context=True)
    async def cuddle(self, ctx, member:disnake.Member=None):
        if member is None or member == ctx.author:
            target = "themselves"
        else:
            target = member.mention

        gifs = os.listdir(f"./RP/cuddle/")
        if gifs == []:
            return

        rnd_gif = choice(gifs)
        path_to_gif = f"./RP/cuddle/{rnd_gif}"
        file = disnake.File(path_to_gif, filename="gif.gif")

        kiss_embed = disnake.Embed(
            title="",
            description=f"{ctx.author.mention} cuddled with {target}",
        )
        kiss_embed.set_image(url="attachment://gif.gif")

        await ctx.send(embed=kiss_embed, file=file)

    @commands.command(pass_context=True)
    async def dance(self, ctx, member:disnake.Member=None):
        if member is None or member == ctx.author:
            target = "themselves"
        else:
            target = member.mention

        gifs = os.listdir(f"./RP/dance/")
        if gifs == []:
            return

        rnd_gif = choice(gifs)
        path_to_gif = f"./RP/dance/{rnd_gif}"
        file = disnake.File(path_to_gif, filename="gif.gif")

        kiss_embed = disnake.Embed(
            title="",
            description=f"{ctx.author.mention} danced with {target}",
        )
        kiss_embed.set_image(url="attachment://gif.gif")

        await ctx.send(embed=kiss_embed, file=file)

    @commands.command(pass_context=True)
    async def handhold(self, ctx, member:disnake.Member=None):
        if member is None or member == ctx.author:
            target = "themselves"
        else:
            target = member.mention

        gifs = os.listdir(f"./RP/handhold/")
        if gifs == []:
            return

        rnd_gif = choice(gifs)
        path_to_gif = f"./RP/handhold/{rnd_gif}"
        file = disnake.File(path_to_gif, filename="gif.gif")

        kiss_embed = disnake.Embed(
            title="",
            description=f"{ctx.author.mention} held hands with {target}",
        )
        kiss_embed.set_image(url="attachment://gif.gif")

        await ctx.send(embed=kiss_embed, file=file)

    @commands.command(pass_context=True)
    async def hug(self, ctx, member:disnake.Member=None):
        if member is None or member == ctx.author:
            target = "themselves"
        else:
            target = member.mention

        gifs = os.listdir(f"./RP/hug/")
        if gifs == []:
            return

        rnd_gif = choice(gifs)
        path_to_gif = f"./RP/hug/{rnd_gif}"
        file = disnake.File(path_to_gif, filename="gif.gif")

        kiss_embed = disnake.Embed(
            title="",
            description=f"{ctx.author.mention} hugged {target}",
        )
        kiss_embed.set_image(url="attachment://gif.gif")

        await ctx.send(embed=kiss_embed, file=file)

    @commands.command(pass_context=True)
    async def kill(self, ctx, member:disnake.Member=None):
        if member is None or member == ctx.author:
            target = "themselves"
        else:
            target = member.mention

        gifs = os.listdir(f"./RP/kill/")
        if gifs == []:
            return

        rnd_gif = choice(gifs)
        path_to_gif = f"./RP/kill/{rnd_gif}"
        file = disnake.File(path_to_gif, filename="gif.gif")

        kiss_embed = disnake.Embed(
            title="",
            description=f"{ctx.author.mention} killed {target}",
        )
        kiss_embed.set_image(url="attachment://gif.gif")

        await ctx.send(embed=kiss_embed, file=file)

    @commands.command(pass_context=True)
    async def kiss(self, ctx, member:disnake.Member=None):
        if member is None or member == ctx.author:
            target = "themselves"
        else:
            target = member.mention

        gifs = os.listdir(f"./RP/kiss/")
        if gifs == []:
            return

        rnd_gif = choice(gifs)
        path_to_gif = f"./RP/kiss/{rnd_gif}"
        file = disnake.File(path_to_gif, filename="gif.gif")

        kiss_embed = disnake.Embed(
            title="",
            description=f"{ctx.author.mention} kissed {target}",
        )
        kiss_embed.set_image(url="attachment://gif.gif")

        await ctx.send(embed=kiss_embed, file=file)

    @commands.command(pass_context=True)
    async def nom(self, ctx, member:disnake.Member=None):
        if member is None or member == ctx.author:
            target = "themselves"
        else:
            target = member.mention

        gifs = os.listdir(f"./RP/nom/")
        if gifs == []:
            return

        rnd_gif = choice(gifs)
        path_to_gif = f"./RP/nom/{rnd_gif}"
        file = disnake.File(path_to_gif, filename="gif.gif")

        kiss_embed = disnake.Embed(
            title="",
            description=f"{ctx.author.mention} took a bite of {target}",
        )
        kiss_embed.set_image(url="attachment://gif.gif")

        await ctx.send(embed=kiss_embed, file=file)

    @commands.command(pass_context=True)
    async def pat(self, ctx, member:disnake.Member=None):
        if member is None or member == ctx.author:
            target = "themselves"
        else:
            target = member.mention

        gifs = os.listdir(f"./RP/pat/")
        if gifs == []:
            return

        rnd_gif = choice(gifs)
        path_to_gif = f"./RP/pat/{rnd_gif}"
        file = disnake.File(path_to_gif, filename="gif.gif")

        kiss_embed = disnake.Embed(
            title="",
            description=f"{ctx.author.mention} patted {target}",
        )
        kiss_embed.set_image(url="attachment://gif.gif")

        await ctx.send(embed=kiss_embed, file=file)

    @commands.command(pass_context=True)
    async def punch(self, ctx, member:disnake.Member=None):
        if member is None or member == ctx.author:
            target = "themselves"
        else:
            target = member.mention

        gifs = os.listdir(f"./RP/punch/")
        if gifs == []:
            return

        rnd_gif = choice(gifs)
        path_to_gif = f"./RP/punch/{rnd_gif}"
        file = disnake.File(path_to_gif, filename="gif.gif")

        kiss_embed = disnake.Embed(
            title="",
            description=f"{ctx.author.mention} punched {target}",
        )
        kiss_embed.set_image(url="attachment://gif.gif")

        await ctx.send(embed=kiss_embed, file=file)

    @commands.command(pass_context=True)
    async def slap(self, ctx, member:disnake.Member=None):
        if member is None or member == ctx.author:
            target = "themselves"
        else:
            target = member.mention

        gifs = os.listdir(f"./RP/slap/")
        if gifs == []:
            return

        rnd_gif = choice(gifs)
        path_to_gif = f"./RP/slap/{rnd_gif}"
        file = disnake.File(path_to_gif, filename="gif.gif")

        kiss_embed = disnake.Embed(
            title="",
            description=f"{ctx.author.mention} slapped {target}",
        )
        kiss_embed.set_image(url="attachment://gif.gif")

        await ctx.send(embed=kiss_embed, file=file)

    @commands.command(pass_context=True)
    async def smile(self, ctx, member:disnake.Member=None):
        if member is None or member == ctx.author:
            target = "themselves"
        else:
            target = member.mention

        gifs = os.listdir(f"./RP/smile/")
        if gifs == []:
            return

        rnd_gif = choice(gifs)
        path_to_gif = f"./RP/smile/{rnd_gif}"
        file = disnake.File(path_to_gif, filename="gif.gif")

        kiss_embed = disnake.Embed(
            title="",
            description=f"{ctx.author.mention} smiled at {target}",
        )
        kiss_embed.set_image(url="attachment://gif.gif")

        await ctx.send(embed=kiss_embed, file=file)

def setup(client):
    client.add_cog(Roleplay(client))
    print(f"Cog: Roleplay - loaded.")

def teardown(client):
    print(f"Cog: Roleplay - unloaded.")