import asyncio
import json
from datetime import datetime as dt

import disnake
import pyrebase
from disnake.ext import commands, tasks
from disnake.ext.commands import guild_only

# //TODO remove unneeded imports and lines of code
# //TODO optimize listeners so multiple listeners are in one decorator

firebase = pyrebase.initialize_app(json.load(open("firebase_config.json", "r")))
db = firebase.database()

guild_id = 940292707102900244

member_counter_id = 966475502095314954
message_counter_id = 966475704743104535
vc_counter_id = 966475555224584212

ignored_guild_id = 382607480410210304


class Counters(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.msg_buffer = 1

    @commands.Cog.listener()
    async def on_ready(self):
        await asyncio.sleep(1)
        if self.update_vc.is_running() == False:
            #print("Counters - Starting loop: update_vc")
            self.update_vc.start()
        else:
            return
        if self.reset.is_running() == False:
            #print("Counters - Starting loop: reset\n")
            self.reset.start()
        else:
            return

    @tasks.loop(hours=1.0, reconnect = True)
    async def reset(self):
        time = dt.now().strftime("%d/%m/%Y %H:%M:%S")
        hour = dt.now().hour
        # print(hour)

        msgCounter = await self.client.fetch_channel(message_counter_id)
        joinCounter = await self.client.fetch_channel(member_counter_id)

        if hour == 0:
            db.child("COUNTERS").child("MEMBERS_JOINED").set(0)
            db.child("COUNTERS").child("MESSAGES_SENT").set(0)
            self.msg_buffer = 1

            await msgCounter.edit(name="Msgs Today • 0")
            await joinCounter.edit(name="Joined Today • 0")

            # print(f"\nCounters: reset at - {time}")

    @tasks.loop(minutes=2.0, reconnect = True)
    async def update_vc(self):
        await asyncio.sleep(1)
        guild = self.client.get_guild(guild_id)
        channel = guild.get_channel(vc_counter_id)
        count = 0
        for vc in guild.voice_channels:
            for member in vc.members:
                if not member.bot:
                    count += 1
        await asyncio.sleep(1)
        #print(f"VC: {count}")
        await channel.edit(name=f"VC members • {count}")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await asyncio.sleep(2)
        if member.bot:
            return

        if member.guild.id == guild_id:
            joinCounter = await self.client.fetch_channel(member_counter_id)
            await asyncio.sleep(1)
            p = db.child("COUNTERS").child("MEMBERS_JOINED").get().val() + 1
            await asyncio.sleep(1)
            await joinCounter.edit(name=f"Joined Today • {p}")
            db.child("COUNTERS").child("MEMBERS_JOINED").set(p)
            #print("Added: +1")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await asyncio.sleep(2)
        if member.bot:
            return

        if member.guild.id == guild_id:
            joinCounter = await self.client.fetch_channel(member_counter_id)
            await asyncio.sleep(1)
            p = db.child("COUNTERS").child("MEMBERS_JOINED").get().val() - 1
            await asyncio.sleep(1)
            await joinCounter.edit(name=f"Joined Today • {p}")
            db.child("COUNTERS").child("MEMBERS_JOINED").set(p)
            #print("Removed: -1")

    @commands.Cog.listener()
    async def on_message(self, message):
        await asyncio.sleep(2)
        msgCounter = await self.client.fetch_channel(message_counter_id)

        try:
            if not isinstance(message, disnake.DMChannel):
                guild = await self.client.fetch_guild(guild_id)
                if message.author.bot or message.guild.id == ignored_guild_id:
                    return

                #print(f"Messages: {self.msg_buffer}")
                if self.msg_buffer >= 10:
                    msgs = db.child("COUNTERS").child("MESSAGES_SENT").get().val()
                    msgs += self.msg_buffer
                    self.msg_buffer = 1
                    db.child("COUNTERS").child("MESSAGES_SENT").set(msgs)
                    await asyncio.sleep(1)
                    await msgCounter.edit(name=f"Msgs Today • {msgs}")
                else:
                    self.msg_buffer += 1
        except AttributeError:
            return

def setup(client):
    client.add_cog(Counters(client))
    print(f"Cog: Counters - loaded.")

def teardown(client):
    print(f"Cog: Counters - unloaded.")