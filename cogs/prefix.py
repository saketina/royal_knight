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

    def get_prefix(self, uid):
        pfxs = db.child("PREFIX").child(uid).get().val()
        if pfxs == None:
            pfxs = []
        return list(pfxs)

    def add_prefix(self, uid, pf):
        pfxs = db.child("PREFIX").child(uid).get().val()
        if pfxs == None:
            pfxs = []
        pfxs.append(pf)
        db.child("PREFIX").child(uid).set(pfxs)

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return
        user = str(msg.author.id)
        prefixes = self.get_prefix(user)
        #print(msg.content)
        for pfix in prefixes:
            check = pfix + "\u0020"
            #print(str(check))
            if msg.content.startswith(check):
                msg.content = msg.content.replace(check, 'k.', 1)
                #msg.content = msg.content.replace("k. ", 'k.')
                await self.client.process_commands(msg)
            elif msg.content.startswith(pfix):
                msg.content = msg.content.replace(pfix, 'k.', 1)
                #msg.content = msg.content.replace("k. ", 'k.')
                await self.client.process_commands(msg)
            elif msg.content.startswith("k. "):
                msg.content = msg.content.replace("k. ", 'k.', 1)
                #msg.content = msg.content.replace("k. ", 'k.')
                await self.client.process_commands(msg)
            

    @commands.command()
    async def prefix(self, ctx, do="", prfx=""):
        user = str(ctx.author.id)
        pfxs = db.child("PREFIX").child(user).get().val()

        if do == "add" and prfx != "":
            if pfxs == None and prfx != "k.":
                self.add_prefix(user, prfx)
                await ctx.send(f"> added custom prefix - `{prfx}`")
            elif prfx not in pfxs and prfx != "k.":
                self.add_prefix(user, prfx)
                await ctx.send(f"> added custom prefix - `{prfx}`")
            else:
                await ctx.send("That prefix is already in the list.")

        elif do == "remove" and prfx != "":
            if pfxs == None:
                pfxs = []
            if prfx not in pfxs:
                await ctx.send("That prefix isn\'t in your prefix list.")
            else:
                del pfxs[pfxs.index(prfx)]
                db.child("PREFIX").child(user).set(pfxs)
                await ctx.send(f"> removed custom prefix - `{prfx}`")
        else:
            e = disnake.Embed(
                title="CUSTOM PREFIXES",
                description="add : add a custom prefix\n"
                            "remove : remove a custom prefix\n\n"
                            "Examples\n"
                            "`k.prefix add <your prefix>`\n"
                            "`k.prefix remove <your prefix>`",
                color=disnake.Color.dark_red()
                )
            ypfx = ""
            all_pfx = self.get_prefix(str(ctx.author.id))
            if all_pfx == []:
                ypfx = "You haven\'t set any prefixes yet."
            for each in all_pfx:
                ypfx += each+"\n"
            e.add_field(
                name="YOUR PREFIXES",
                value=ypfx
                )
            await ctx.send(embed=e)

    @prefix.error
    async def prefix_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("I can\'t find that in the list.")
        else:
            print(error)

def setup(client):
    client.add_cog(Prefix(client))
    print(f"Cog: Prefix - loaded.")

def teardown(client):
    print(f"Cog: Prefix - unloaded.")
