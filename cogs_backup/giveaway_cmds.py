import disnake
from disnake.ext import commands
from datetime import datetime as dt
import pyrebase
import json
from random import choices

firebase = pyrebase.initialize_app(
    json.load(open("firebase_config.json", "r")))
db = firebase.database()


def get_total_entries(data):  # gets the total entries form db
    t = 0
    for id_ in data:
        t += data[id_]
    return t


# converts data to data with probabilities according to entries
def get_data_with_probabilities(data, total_entries):
    data_with_probs = {}
    for id_ in data:
        data_with_probs[id_] = data[id_] / total_entries
    return data_with_probs


def roll():
    data = db.child("ENTRIES").get().val()
    total_entries = get_total_entries(dict(data))
    data_weighted = get_data_with_probabilities(data, total_entries)
    ids = list(data_weighted.keys())
    weights = tuple(data_weighted.values())
    return choices(ids, weights=weights, k=1)


class GiveawayCmds(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def entries(self, ctx, user: disnake.User = None):
        if user == None:
            user = ctx.author

        all_entries = db.child("ENTRIES").get().val()

        uid = str(user.id)
        if all_entries == None:
            users_entries = 0
        else:
            all_entries = dict(all_entries)
            if uid in all_entries:
                users_entries = all_entries[uid]
            else:
                users_entries = 0
        emb = disnake.Embed(
            title=f"",
            description=f"{user} has **{users_entries}** entries")
        await ctx.send(embed=emb)

    @commands.command()
    async def giveaway(self, ctx, cmd=""):
        if ctx.author.guild_permissions.administrator:
            cmd = cmd.lower()
            if cmd == "reset":
                await ctx.send(f"{ctx.author.mention} reset all giveaway entries? (y/n)")
                try:
                    msg = await self.client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60.0)
                except Exception:
                    await ctx.send("you took too much time to answer :p")
                    return
                if msg.content.lower() == "y":
                    db.child("ENTRIES").remove()
                    await ctx.send(f"all entries reset :p")
                else:
                    await ctx.send(f"command cancelled")
                return
            elif cmd == "true" or cmd == "1":
                cmd = True
            elif cmd == "false" or cmd == "0":
                cmd = False
            elif cmd == "roll":
                winner_id = roll()[0]
                winner = await ctx.guild.fetch_member(winner_id)
                await ctx.send(f"{winner.mention} is the winner")
                return
            else:
                await ctx.send(f"{ctx.author.mention} you need to pass in either `True` or `False` or `reset` or `roll`\nTrue - enables counting of entries\nFalse - disables counting of entries\nreset - clears all entries\nroll - rolls and gets a winner")
                return
            db.child("SETTINGS").child("GIVEAWAY_ENABLED").set(cmd)
            await ctx.send(f"{ctx.author.mention}\n`GIVEAWAY_ENABLED` set to `{cmd}`")


def setup(client):
    client.add_cog(GiveawayCmds(client))
