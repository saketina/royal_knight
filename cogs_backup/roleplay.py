import disnake
from disnake.ext import commands
from random import choice
import os
import pyrebase
import json

firebase = pyrebase.initialize_app(json.load(open("firebase_config.json", "r")))
db = firebase.database()


class Roleplay(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.got = 0
        self.did = 0

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return


        if message.content.lower().startswith("m!") or message.content.startswith("!"):
            cmd = (
                message.content.replace("M!", "").replace("m!", "").replace("!", "")
                + " "
            )
            rp_cmds = list(map(str.lower, os.listdir("./RP")))
            #print(cmd)
            #print(rp_cmds)
            msg_str = cmd
            mentions = ""
            if len(message.mentions) > 0:
                for mem in message.mentions:
                    if message.mentions.index(mem) == 0:
                        mentions += f" {mem}"
                    elif message.mentions.index(mem) == len(message.mentions) - 1:
                        mentions += f" and {mem}"
                    else:
                        mentions += f", {mem}"
                    msg_str = msg_str.replace(f"<@{mem.id}>", "")
                    msg_str = msg_str.replace(f"<@!{mem.id}>", "")
                #print(mentions)

            msg_broken = cmd.split(" ")
            if msg_broken[0].lower() in rp_cmds:
                cmd = msg_broken[0][0].lower() + msg_broken[0][1:]
                msg_str = msg_str.lower().replace(cmd.lower(), "")
                print(msg_str)
                gifs = os.listdir(f"./RP/{cmd}/")
                if gifs == []:
                    return
                rnd_gif = choice(gifs)
                path_to_gif = f"./RP/{cmd}/{rnd_gif}"
                file = disnake.File(path_to_gif, filename="gif.gif")
                # extra = " ".join(msg_broken[1:])
                extra = mentions
                if len(extra) > 0:
                    extra = "on " + extra
                if len(msg_str.strip()) > 0:
                    msg_str = f'"{msg_str.strip()}"'
                embed = disnake.Embed(
                    title="",
                    description=f"{message.author} used {cmd} {extra}  {msg_str}",
                )
                embed.set_image(url="attachment://gif.gif")
                await message.channel.send(embed=embed, file=file)


def setup(client):
    client.add_cog(Roleplay(client))
