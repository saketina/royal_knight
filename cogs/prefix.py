import json
import disnake
import pyrebase
from disnake.ext import commands

## //TODO: PREFIX_ADD create banned prefixes list

firebase = pyrebase.initialize_app(
    json.load(open("firebase_config.json", "r")))
db = firebase.database()

class Prefix(commands.Cog):
    def __init__(self, client):
        self.client = client

    def get_user_prefixes(self, user_id):
        prefixes = db.child("PREFIX").child(user_id).get().val()
        if prefixes == None:
            prefixes = []
        return list(prefixes)

    def add_user_prefix(self, user_id, new_prefix):
        prefixes = self.get_user_prefixes(user_id)
        if new_prefix not in prefixes and new_prefix != "k.":
            prefixes.append(new_prefix)
            db.child("PREFIX").child(user_id).set(prefixes)

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return
        user_id = str(msg.author.id)
        user_prefixes = self.get_user_prefixes(user_id)

        # Check is space is after prefix
        if msg.content.startswith("k. "):
            msg.content = msg.content.replace("k. ", 'k.', 1)
            await self.client.process_commands(msg)
        elif msg.content.startswith("K. "):
            msg.content = msg.content.replace("K. ", 'k.', 1)
            await self.client.process_commands(msg)
        
        # Check for custom prefixes
        for prefix in user_prefixes:
            check = prefix + '\u0020'
            if msg.content.startswith(check):
                msg.content = msg.content.replace(check, 'k.', 1)
                await self.client.process_commands(msg)
            elif msg.content.startswith(prefix):
                msg.content = msg.content.replace(prefix, 'k.', 1)
                await self.client.process_commands(msg)

    @commands.command()
    async def prefix(self, ctx, action="", new_prefix=""):
        user_id = str(ctx.author.id)
        user_prefixes = self.get_user_prefixes(user_id)

        if action == "add" and new_prefix:
            if new_prefix not in user_prefixes and new_prefix != "k.":
                self.add_user_prefix(user_id, new_prefix)
                await ctx.send(f"> added custom prefix - `{new_prefix}`")
            else:
                await ctx.send("That prefix is already in the list.")

        elif action == "remove" and new_prefix:
            if new_prefix not in user_prefixes:
                await ctx.send("That prefix isn't in your prefix list.")
            else:
                user_prefixes.remove(new_prefix)
                db.child("PREFIX").child(user_id).set(user_prefixes)
                await ctx.send(f"> removed custom prefix - `{new_prefix}`")

        else:
            prefixes_text = "\n".join(user_prefixes) if user_prefixes else "You haven't set any prefixes yet."
            embed = disnake.Embed(
                title="Custom Prefixes",
                description="Add or remove custom prefixes for bot commands.",
                color=disnake.Color.dark_red()
            )
            embed.add_field(
                name="Your Prefixes",
                value=prefixes_text
            )
            embed.add_field(
                name="Usage",
                value="`k.prefix add <your_prefix>`\n`k.prefix remove <your_prefix>`",
                inline=False
            )
            await ctx.send(embed=embed)

    @prefix.error
    async def prefix_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("I can't find that in the list.")
        else:
            print(error)

def setup(client):
    client.add_cog(Prefix(client))
    print(f"Cog: Prefix - loaded.")

def teardown(client):
    print(f"Cog: Prefix - unloaded.")
