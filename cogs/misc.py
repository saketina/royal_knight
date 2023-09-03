import asyncio

import disnake
from disnake.ext import commands


class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content == "80085":
            await message.channel.send("Wow! You found them.")
            await asyncio.sleep(4)
            await message.channel.send("Sadly not in real life...")

    @commands.command(pass_context=True)
    #@has_permissions(administrator=True)
    async def status(self, ctx, activity=None, *, text=None):
        if activity == "playing":
            act = disnake.Activity(type=disnake.ActivityType.playing, name=text)
            response = "Playing"
            await self.client.change_presence(activity=act, status=disnake.Status.dnd)
            await ctx.send(f"Status changed to `{response} {text}`")

        elif activity == "streaming":
            act = disnake.Activity(type=disnake.ActivityType.streaming, name=text)
            response = "Streaming"
            await self.client.change_presence(activity=act, status=disnake.Status.dnd)
            await ctx.send(f"Status changed to `{response} {text}`")

        elif activity == "watching":
            act = disnake.Activity(type=disnake.ActivityType.watching, name=text)
            response = "Watching"
            await self.client.change_presence(activity=act, status=disnake.Status.dnd)
            await ctx.send(f"Status changed to `{response} {text}`")

        elif activity == "competing":
            act = disnake.Activity(type=disnake.ActivityType.competing, name=text)
            response = "Competing in"
            await self.client.change_presence(activity=act, status=disnake.Status.dnd)
            await ctx.send(f"Status changed to `{response} {text}`")

        elif activity == "remove":
            act = disnake.Activity(type=disnake.ActivityType.custom, name=None)
            await self.client.change_presence(activity=act, status=disnake.Status.dnd)
            await ctx.send(f"Status changed to `{text}`")

        elif activity==None or text==None:
            embed = disnake.Embed(
            title="STATUS HELP",
            description="``k.status [activity] [text]``",
            color = disnake.Color.dark_red()
            )
            embed.add_field(
            name="Activity",
            value="playing" + "\n" +
                  "streaming" + "\n" +
                  "watching" + "\n" +
                  "competing" + "\n" +
                  "remove"
            )

            await ctx.send(embed=embed)
        else:
            await ctx.send("I didn\'t quite catch that.")


def setup(client):
    client.add_cog(Misc(client))
    print(f"Cog: Misc - loaded.")

def teardown(client):
    print(f"Cog: Misc - unloaded.")
