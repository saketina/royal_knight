import disnake
from disnake.ext import commands
from datetime import datetime as dt
import pyrebase
import json

firebase = pyrebase.initialize_app(json.load(open("firebase_config.json", "r")))
db = firebase.database()

general_id = 960372132204912650
sora_guild_id = 940292707102900244


def add_entry(uid):
    # adds am entry for the user in DB
    all_entries = db.child("ENTRIES").get().val()
    if all_entries == None:
        db.child("ENTRIES").child(uid).set(1)
        return
    else:
        all_entries = dict(all_entries)
        if uid in all_entries:
            users_entries = all_entries[uid]
            db.child("ENTRIES").child(uid).set(users_entries + 1)  # increment entries
        else:
            db.child("ENTRIES").child(uid).set(1)
    # print(entries)


class Giveaway(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.msg_count = {}  # {user_id:(count,datetime)}

    @commands.Cog.listener()
    async def on_message(self, message):
        # stop if giveaway enabled is false
        if not db.child("SETTINGS").child("GIVEAWAY_ENABLED").get().val():
            return
        # ignore bots and other server
        if message.author or message.guild.id == sora_guild_id:
            return
        # if channel isnt general or user is admin, stop
        if (
            message.channel.id != general_id
            or message.author.guild_permissions.administrator
        ):
            return
        # if message.channel.id != 750297459246366779: ## BOT TESTING CHANNEL
        # return
        user_id = str(message.author.id)
        # print(user_id)
        if user_id in list(self.msg_count):
            count = self.msg_count[user_id][0]
            print(count)
            time_old = self.msg_count[user_id][1]
            time_now = dt.now()
            difference = time_now - time_old
            # print(difference.total_seconds())
            if difference.total_seconds() >= 60:
                if count >= 90:
                    add_entry(user_id)
                    count = 0
                    self.msg_count[user_id] = (count, time_now)
                else:
                    count += 1
                    self.msg_count[user_id] = (count, time_now)
        else:
            add_entry(user_id)
            count = 1
            time = dt.now()
            self.msg_count[user_id] = (count, time)
        print(self.msg_count)


def setup(client):
    client.add_cog(Giveaway(client))
