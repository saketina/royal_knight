import json
import os
import time
from datetime import timedelta
from io import BytesIO
from random import choice

import disnake
import PIL
import pyrebase
from disnake.ext import commands
from PIL import Image

import logging

logging = logging.getLogger("Roleplay")

# TODO ALL/make different gifs displayed if ctx.author used the command on themselves
# TODO resize gifs to 498x278
# TODO ADD wave, sip, shoot command

firebase = pyrebase.initialize_app(json.load(open("./firebase_config.json", "r")))
db = firebase.database()

def load_gif(command, last_gif):

    gifs = os.listdir(f"./RP/{command}/")
    if gifs == []:
        return

    gif_image = Image.open(f"./RP/{command}/{last_gif}")
    image_bytes = BytesIO()
    gif_image.resize((500, 264))
    gif_image.tobytes()
    gif_image.save(image_bytes, format="GIF", save_all=True)
    image_bytes.seek(0)
    #logging.info(image_bytes)
    gif_image.close()
    return image_bytes

def per_cmd_loader(folder):
    loaded_gifs = {}
    gifs = []
    files = os.listdir(f"./RP/{folder}")
    #logging.info(files)
    for file_name in files:
        #logging.info("done")
        # Get the full path to the GIF
        #gif_path = os.path.join(root, file_name)

        # Open the GIF using Pillow
        gif_im = Image.open(f"./RP/bite/{file_name}")
        #image_byt = ""
        #image_byt = BytesIO()
        gif_im.resize((500, 264))
        #gif_im.tobytes()
        #gif_im.save(image_byt, format="GIF", save_all=True)
        #image_byt.seek(0)
        #logging.info(gif_im)

        gifs.append(gif_im)
                

    loaded_gifs = gifs
    #logging.info(loaded_gifs)

    #logging.info(loaded_gifs)
    #logging.info(loaded_gifs)
    logging.info("gifs have been preloaded")
    return loaded_gifs  # Return the dictionary of processed GIFs

class Roleplay(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.rp_last = None
        self.gifs = {}

        self.bite_last = None
        self.blush_last = None
        self.bonk_last = None
        self.boop_last = None
        self.cry_last = None
        self.cuddle_last = None
        self.dance_last = None
        self.handhold_last = None
        self.hug_last = None
        self.kill_last = None
        self.kiss_last = None
        self.nom_last = None
        self.pat_last = None
        self.punch_last = None
        self.slap_last = None
        self.smile_last = None

    def gif_loading(self, gif_folder):
        loaded_gifs = {}  # Create a dictionary to store the GIFs

        subfolders = [f for f in os.listdir(gif_folder) if os.path.isdir(os.path.join(gif_folder, f))]
        #logging.info(subfolders)
        #for folder_name in subfolders:
        #    folder_path = os.path.join(gif_folder, folder_name)
        gifs = []

        #for root, _, files in os.walk(folder_path):
        files = os.listdir("./RP/bite")
        logging.info(files)
        for file_name in files:
            logging.info("done")
            # Get the full path to the GIF
            #gif_path = os.path.join(root, file_name)

            # Open the GIF using Pillow
            gif_image = Image.open(f"./RP/bite/{file_name}")
            image_bytes = BytesIO()
            gif_image.resize((500, 264))
            #gif_image.tobytes()
            gif_image.save(image_bytes, format="GIF", save_all=True)
            image_bytes.seek(0)

            gifs.append(image_bytes)
            #gif_image.close()
                    

        loaded_gifs['bite'] = gifs
        logging.info(loaded_gifs)

        self.gifs[gif_folder] = loaded_gifs

        logging.info("gifs have been preloaded")
        #return loaded_gifs  # Return the dictionary of processed GIFs
        return

    @commands.command()
    async def gif_load(self, ctx):
        """
        rp = os.listdir("./RP")
        for command in rp:
            loaded_gifs = gif_loading(command)

            logging.info(gifs)
            self.gifs[command]=loaded_gifs
            logging.info("gay")
            logging.info(gifs)
            await ctx.send(f"GIFs loaded for command '{command}'")
        logging.info("done")"""
        # Check if the specified directory exists
        if not os.path.exists("./RP"):
            await ctx.send(f"The folder RP does not exist.")
            return

        gifs = load_gif(f"./RP/")
        await ctx.send("GIFs loaded and stored.")
        #logging.info(gifs)

    @commands.command(pass_context=True)
    async def bite(self, ctx, member:disnake.Member=None):
        start_time = time.monotonic()
        if member is None or member == ctx.author:
            target = "themselves"
            db_target = "SELF"
            member = ctx.author
        else:
            target = member.mention
            db_target = "OTHER"

        try:
            #logging.info(self.gifs[ctx.command.qualified_name])
            loaded_gifs = self.gifs[ctx.command.qualified_name]
            #logging.info("sexy bitches")
        except KeyError:
            loaded_gifs = per_cmd_loader(ctx.command.qualified_name)
            #logging.info(f"loaded gifs in {ctx.command.qualified_name}")
            gifs = self.gifs[ctx.command.qualified_name] = loaded_gifs
            #logging.info("gifs preloaded in command/bite")

        async with ctx.typing():
            rnd_gif = choice(loaded_gifs)
            #logging.info(self.gifs)

            try:
                last = self.rp_last[ctx.command.qualified_name]
            except:
                last = ""

            while rnd_gif == last:
                rnd_gif = choice(self.gifs)

            gif_im = rnd_gif
            #image_byt = ""
            image_byt = BytesIO()
            #gif_im.resize((500, 264))
            #gif_im.tobytes()
            #logging.info(gif_im)
            gif = gif_im.save(image_byt, format="GIF", save_all=True)
            image_byt.seek(0)
            #logging.info(image_byt)

            
            file = disnake.File(image_byt, filename="gif.gif")

            kiss_embed = disnake.Embed(
                title="",
                description=f"{ctx.author.mention} bit {target}",
            )
            kiss_embed.set_image(url="attachment://gif.gif")

            rp_db = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).get().val()
            if rp_db == None:
                db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).set(1)
            elif rp_db != None:
                p = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).get().val() + 1
                db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).set(p)
            else:
                await ctx.send("Rarest error ever, please contact developer!!!")

            self_num = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child("SELF").get().val()
            other_num = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child("OTHER").get().val()

            if other_num == None:
                other_time = "times"
                other_num = 0
            elif other_num > 1:
                other_time = "times"
            else:
                other_time = "time"
                
            if self_num == None:
                self_time = "times"
                self_num = 0
            elif self_num > 1:
                self_time = "times"
            else:
                self_time = "time"

            kiss_embed.set_footer(text=f"Others: {other_num} {other_time}\nThemselves: {self_num} {self_time}")
            self.rp_last: ctx.command.name=gif
        await ctx.send(embed=kiss_embed, file=file)
        image_byt.close()
        #rnd_gif.close()
        end_time = time.monotonic()
        logging.info(f"{ctx.command.qualified_name}\n{timedelta(seconds = end_time - start_time)}")

    @commands.command(pass_context=True)
    async def blush(self, ctx, member:disnake.Member=None):
        start_time = time.monotonic()
        if member is None or member == ctx.author:
            target = "themselves"
            db_target = "SELF"
            member = ctx.author
        else:
            target = member.mention
            db_target = "OTHER"

        gifs = os.listdir(f"./RP/blush/")
        if gifs == []:
            return

        rnd_gif = choice(gifs)

        while rnd_gif == self.blush_last:
            rnd_gif = choice(gifs)
        
        path_to_gif = f"./RP/blush/{rnd_gif}"
        file = disnake.File(path_to_gif, filename="gif.gif")

        kiss_embed = disnake.Embed(
            title="",
            description=f"{ctx.author.mention} blushed at {target}",
        )
        kiss_embed.set_image(url="attachment://gif.gif")

        rp_db = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).get().val()
        if rp_db == None:
            db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).set(1)
        elif rp_db != None:
            p = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).get().val() + 1
            db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).set(p)
        else:
            await ctx.send("Rarest error ever, please contact developer!!!")

        self_num = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child("SELF").get().val()
        other_num = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child("OTHER").get().val()

        if other_num == None:
            other_time = "times"
            other_num = 0
        elif other_num > 1:
            other_time = "times"
        else:
            other_time = "time"
            
        if self_num == None:
            self_time = "times"
            self_num = 0
        elif self_num > 1:
            self_time = "times"
        else:
            self_time = "time"

        kiss_embed.set_footer(text=f"Others: {other_num} {other_time}\nThemselves: {self_num} {self_time}")
        self.blush_last = rnd_gif
        await ctx.send(embed=kiss_embed, file=file)
        end_time = time.monotonic()
        logging.info(f"blush\n{timedelta(seconds = end_time - start_time)}")

    @commands.command(pass_context=True)
    async def bonk(self, ctx, member:disnake.Member=None):
        if member is None or member == ctx.author:
            target = "themselves"
            db_target = "SELF"
            member = ctx.author
        else:
            target = member.mention
            db_target = "OTHER"

        gifs = os.listdir(f"./RP/bonk/")
        if gifs == []:
            return

        rnd_gif = choice(gifs)

        while rnd_gif == self.bonk_last:
            rnd_gif = choice(gifs)
        
        path_to_gif = f"./RP/bonk/{rnd_gif}"
        file = disnake.File(path_to_gif, filename="gif.gif")

        kiss_embed = disnake.Embed(
            title="",
            description=f"{ctx.author.mention} bonked {target}",
        )
        kiss_embed.set_image(url="attachment://gif.gif")

        rp_db = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).get().val()
        if rp_db == None:
            db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).set(1)
        elif rp_db != None:
            p = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).get().val() + 1
            db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).set(p)
        else:
            await ctx.send("Rarest error ever, please contact developer!!!")

        self_num = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child("SELF").get().val()
        other_num = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child("OTHER").get().val()

        if other_num == None:
            other_time = "times"
            other_num = 0
        elif other_num > 1:
            other_time = "times"
        else:
            other_time = "time"
            
        if self_num == None:
            self_time = "times"
            self_num = 0
        elif self_num > 1:
            self_time = "times"
        else:
            self_time = "time"

        kiss_embed.set_footer(text=f"Others: {other_num} {other_time}\nThemselves: {self_num} {self_time}")
        self.bonk_last = rnd_gif
        await ctx.send(embed=kiss_embed, file=file)

    @commands.command(pass_context=True)
    async def boop(self, ctx, member:disnake.Member=None):
        if member is None or member == ctx.author:
            target = "themselves"
            db_target = "SELF"
            member = ctx.author
        else:
            target = member.mention
            db_target = "OTHER"

        gifs = os.listdir(f"./RP/boop/")
        if gifs == []:
            return

        rnd_gif = choice(gifs)

        while rnd_gif == self.boop_last:
            rnd_gif = choice(gifs)
        
        path_to_gif = f"./RP/boop/{rnd_gif}"
        file = disnake.File(path_to_gif, filename="gif.gif")

        kiss_embed = disnake.Embed(
            title="",
            description=f"{ctx.author.mention} booped {target}",
        )
        kiss_embed.set_image(url="attachment://gif.gif")

        rp_db = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).get().val()
        if rp_db == None:
            db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).set(1)
        elif rp_db != None:
            p = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).get().val() + 1
            db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).set(p)
        else:
            await ctx.send("Rarest error ever, please contact developer!!!")

        self_num = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child("SELF").get().val()
        other_num = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child("OTHER").get().val()
        logging.info(self_num, other_num)

        if other_num == None:
            other_time = "times"
            other_num = 0
        elif other_num > 1:
            other_time = "times"
        else:
            other_time = "time"
            
        if self_num == None:
            self_time = "times"
            self_num = 0
        elif self_num > 1:
            self_time = "times"
        else:
            self_time = "time"

        kiss_embed.set_footer(text=f"Others: {other_num} {other_time}\nThemselves: {self_num} {self_time}")
        self.boop_last = rnd_gif
        await ctx.send(embed=kiss_embed, file=file)

    @commands.command(pass_context=True)
    async def cry(self, ctx, member:disnake.Member=None):
        if member is None or member == ctx.author:
            target = "themselves"
            db_target = "SELF"
            member = ctx.author
        else:
            target = member.mention
            db_target = "OTHER"

        gifs = os.listdir(f"./RP/cry/")
        if gifs == []:
            return

        rnd_gif = choice(gifs)

        while rnd_gif == self.cry_last:
            rnd_gif = choice(gifs)
        
        path_to_gif = f"./RP/cry/{rnd_gif}"
        file = disnake.File(path_to_gif, filename="gif.gif")

        kiss_embed = disnake.Embed(
            title="",
            description=f"{ctx.author.mention} cried at {target}",
        )
        kiss_embed.set_image(url="attachment://gif.gif")

        rp_db = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).get().val()
        if rp_db == None:
            db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).set(1)
        elif rp_db != None:
            p = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).get().val() + 1
            db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).set(p)
        else:
            await ctx.send("Rarest error ever, please contact developer!!!")

        self_num = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child("SELF").get().val()
        other_num = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child("OTHER").get().val()

        if other_num == None:
            other_time = "times"
            other_num = 0
        elif other_num > 1:
            other_time = "times"
        else:
            other_time = "time"
            
        if self_num == None:
            self_time = "times"
            self_num = 0
        elif self_num > 1:
            self_time = "times"
        else:
            self_time = "time"

        kiss_embed.set_footer(text=f"Others: {other_num} {other_time}\nThemselves: {self_num} {self_time}")
        self.cry_last = rnd_gif
        await ctx.send(embed=kiss_embed, file=file)

    @commands.command(pass_context=True)
    async def cuddle(self, ctx, member:disnake.Member=None):
        if member is None or member == ctx.author:
            target = "themselves"
            db_target = "SELF"
            member = ctx.author
        else:
            target = member.mention
            db_target = "OTHER"

        gifs = os.listdir(f"./RP/cuddle/")
        if gifs == []:
            return

        rnd_gif = choice(gifs)

        while rnd_gif == self.cuddle_last:
            rnd_gif = choice(gifs)
        
        path_to_gif = f"./RP/cuddle/{rnd_gif}"
        file = disnake.File(path_to_gif, filename="gif.gif")

        kiss_embed = disnake.Embed(
            title="",
            description=f"{ctx.author.mention} cuddled with {target}",
        )
        kiss_embed.set_image(url="attachment://gif.gif")

        rp_db = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).get().val()
        if rp_db == None:
            db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).set(1)
        elif rp_db != None:
            p = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).get().val() + 1
            db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).set(p)
        else:
            await ctx.send("Rarest error ever, please contact developer!!!")

        self_num = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child("SELF").get().val()
        other_num = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child("OTHER").get().val()

        if other_num == None:
            other_time = "times"
            other_num = 0
        elif other_num > 1:
            other_time = "times"
        else:
            other_time = "time"
            
        if self_num == None:
            self_time = "times"
            self_num = 0
        elif self_num > 1:
            self_time = "times"
        else:
            self_time = "time"

        kiss_embed.set_footer(text=f"Others: {other_num} {other_time}\nThemselves: {self_num} {self_time}")
        self.cuddle_last = rnd_gif
        await ctx.send(embed=kiss_embed, file=file)

    @commands.command(pass_context=True)
    async def dance(self, ctx, member:disnake.Member=None):
        if member is None or member == ctx.author:
            target = "themselves"
            db_target = "SELF"
            member = ctx.author
        else:
            target = member.mention
            db_target = "OTHER"

        gifs = os.listdir(f"./RP/dance/")
        if gifs == []:
            return

        rnd_gif = choice(gifs)

        while rnd_gif == self.dance_last:
            rnd_gif = choice(gifs)
        
        path_to_gif = f"./RP/dance/{rnd_gif}"
        file = disnake.File(path_to_gif, filename="gif.gif")

        kiss_embed = disnake.Embed(
            title="",
            description=f"{ctx.author.mention} danced with {target}",
        )
        kiss_embed.set_image(url="attachment://gif.gif")

        rp_db = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).get().val()
        if rp_db == None:
            db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).set(1)
        elif rp_db != None:
            p = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).get().val() + 1
            db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).set(p)
        else:
            await ctx.send("Rarest error ever, please contact developer!!!")

        self_num = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child("SELF").get().val()
        other_num = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child("OTHER").get().val()

        if other_num == None:
            other_time = "times"
            other_num = 0
        elif other_num > 1:
            other_time = "times"
        else:
            other_time = "time"
            
        if self_num == None:
            self_time = "times"
            self_num = 0
        elif self_num > 1:
            self_time = "times"
        else:
            self_time = "time"

        kiss_embed.set_footer(text=f"Others: {other_num} {other_time}\nThemselves: {self_num} {self_time}")
        self.dance_last = rnd_gif
        await ctx.send(embed=kiss_embed, file=file)

    @commands.command(pass_context=True)
    async def fuck(self, ctx, member:disnake.Member=None):
        if member is None or member == ctx.author:
            target = "themselves"
            db_target = "SELF"
            member = ctx.author
        else:
            target = member.mention
            db_target = "OTHER"


        path_to_gif = f"./RP/fuck/fuck.gif"
        file = disnake.File(path_to_gif, filename="gif.gif")

        kiss_embed = disnake.Embed(
            title="",
            description=f"{ctx.author.mention} fucked with {target}",
        )
        kiss_embed.set_image(url="attachment://gif.gif")

        rp_db = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).get().val()
        if rp_db == None:
            db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).set(1)
        elif rp_db != None:
            p = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).get().val() + 1
            db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).set(p)
        else:
            await ctx.send("Rarest error ever, please contact developer!!!")

        self_num = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child("SELF").get().val()
        other_num = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child("OTHER").get().val()

        if other_num == None:
            other_time = "times"
            other_num = 0
        elif other_num > 1:
            other_time = "times"
        else:
            other_time = "time"
            
        if self_num == None:
            self_time = "times"
            self_num = 0
        elif self_num > 1:
            self_time = "times"
        else:
            self_time = "time"

        kiss_embed.set_footer(text=f"Others: {other_num} {other_time}\nThemselves: {self_num} {self_time}")

        await ctx.send(embed=kiss_embed, file=file)

    @commands.command(pass_context=True)
    async def handhold(self, ctx, member:disnake.Member=None):
        if member is None or member == ctx.author:
            target = "themselves"
            db_target = "SELF"
            member = ctx.author
        else:
            target = member.mention
            db_target = "OTHER"

        gifs = os.listdir(f"./RP/handhold/")
        if gifs == []:
            return

        rnd_gif = choice(gifs)

        while rnd_gif == self.handhold_last:
            rnd_gif = choice(gifs)
        
        path_to_gif = f"./RP/handhold/{rnd_gif}"
        file = disnake.File(path_to_gif, filename="gif.gif")

        kiss_embed = disnake.Embed(
            title="",
            description=f"{ctx.author.mention} held hands with {target}",
        )
        kiss_embed.set_image(url="attachment://gif.gif")

        rp_db = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).get().val()
        if rp_db == None:
            db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).set(1)
        elif rp_db != None:
            p = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).get().val() + 1
            db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).set(p)
        else:
            await ctx.send("Rarest error ever, please contact developer!!!")

        self_num = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child("SELF").get().val()
        other_num = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child("OTHER").get().val()

        if other_num == None:
            other_time = "times"
            other_num = 0
        elif other_num > 1:
            other_time = "times"
        else:
            other_time = "time"
            
        if self_num == None:
            self_time = "times"
            self_num = 0
        elif self_num > 1:
            self_time = "times"
        else:
            self_time = "time"

        kiss_embed.set_footer(text=f"Others: {other_num} {other_time}\nThemselves: {self_num} {self_time}")
        self.handhold_last = rnd_gif
        await ctx.send(embed=kiss_embed, file=file)

    @commands.command(pass_context=True)
    async def hug(self, ctx, member:disnake.Member=None):
        if member is None or member == ctx.author:
            target = "themselves"
            db_target = "SELF"
            member = ctx.author
        else:
            target = member.mention
            db_target = "OTHER"

        gifs = os.listdir(f"./RP/hug/")
        if gifs == []:
            return

        rnd_gif = choice(gifs)

        while rnd_gif == self.hug_last:
            rnd_gif = choice(gifs)
        
        path_to_gif = f"./RP/hug/{rnd_gif}"
        file = disnake.File(path_to_gif, filename="gif.gif")

        kiss_embed = disnake.Embed(
            title="",
            description=f"{ctx.author.mention} hugged {target}",
        )
        kiss_embed.set_image(url="attachment://gif.gif")

        rp_db = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).get().val()
        if rp_db == None:
            db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).set(1)
        elif rp_db != None:
            p = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).get().val() + 1
            db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).set(p)
        else:
            await ctx.send("Rarest error ever, please contact developer!!!")

        self_num = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child("SELF").get().val()
        other_num = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child("OTHER").get().val()

        if other_num == None:
            other_time = "times"
            other_num = 0
        elif other_num > 1:
            other_time = "times"
        else:
            other_time = "time"
            
        if self_num == None:
            self_time = "times"
            self_num = 0
        elif self_num > 1:
            self_time = "times"
        else:
            self_time = "time"

        kiss_embed.set_footer(text=f"Others: {other_num} {other_time}\nThemselves: {self_num} {self_time}")
        self.hug_last = rnd_gif
        await ctx.send(embed=kiss_embed, file=file)

    @commands.command(pass_context=True)
    async def kill(self, ctx, member:disnake.Member=None):
        if member is None or member == ctx.author:
            target = "themselves"
            db_target = "SELF"
            member = ctx.author
        else:
            target = member.mention
            db_target = "OTHER"

        gifs = os.listdir(f"./RP/kill/")
        if gifs == []:
            return

        rnd_gif = choice(gifs)

        while rnd_gif == self.kill_last:
            rnd_gif = choice(gifs)
        
        path_to_gif = f"./RP/kill/{rnd_gif}"
        file = disnake.File(path_to_gif, filename="gif.gif")

        kiss_embed = disnake.Embed(
            title="",
            description=f"{ctx.author.mention} killed {target}",
        )
        kiss_embed.set_image(url="attachment://gif.gif")

        rp_db = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).get().val()
        if rp_db == None:
            db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).set(1)
        elif rp_db != None:
            p = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).get().val() + 1
            db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).set(p)
        else:
            await ctx.send("Rarest error ever, please contact developer!!!")

        self_num = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child("SELF").get().val()
        other_num = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child("OTHER").get().val()

        if other_num == None:
            other_time = "times"
            other_num = 0
        elif other_num > 1:
            other_time = "times"
        else:
            other_time = "time"
            
        if self_num == None:
            self_time = "times"
            self_num = 0
        elif self_num > 1:
            self_time = "times"
        else:
            self_time = "time"

        kiss_embed.set_footer(text=f"Others: {other_num} {other_time}\nThemselves: {self_num} {self_time}")
        self.kill_last = rnd_gif
        await ctx.send(embed=kiss_embed, file=file)

    @commands.command(pass_context=True)
    async def kiss(self, ctx, member:disnake.Member=None):
        if member is None or member == ctx.author:
            target = "themselves"
            db_target = "SELF"
            member = ctx.author
        else:
            target = member.mention
            db_target = "OTHER"

        gifs = os.listdir(f"./RP/kiss/")
        if gifs == []:
            return

        rnd_gif = choice(gifs)

        while rnd_gif == self.kiss_last:
            rnd_gif = choice(gifs)
        
        path_to_gif = f"./RP/kiss/{rnd_gif}"
        file = disnake.File(path_to_gif, filename="gif.gif")

        kiss_embed = disnake.Embed(
            title="",
            description=f"{ctx.author.mention} kissed {target}",
        )
        kiss_embed.set_image(url="attachment://gif.gif")

        rp_db = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).get().val()
        if rp_db == None:
            db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).set(1)
        elif rp_db != None:
            p = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).get().val() + 1
            db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).set(p)
        else:
            await ctx.send("Rarest error ever, please contact developer!!!")

        self_num = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child("SELF").get().val()
        other_num = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child("OTHER").get().val()

        if other_num == None:
            other_time = "times"
            other_num = 0
        elif other_num > 1:
            other_time = "times"
        else:
            other_time = "time"
            
        if self_num == None:
            self_time = "times"
            self_num = 0
        elif self_num > 1:
            self_time = "times"
        else:
            self_time = "time"

        kiss_embed.set_footer(text=f"Others: {other_num} {other_time}\nThemselves: {self_num} {self_time}")
        self.kiss_last = rnd_gif
        await ctx.send(embed=kiss_embed, file=file)

    @commands.command(pass_context=True)
    async def nom(self, ctx, member:disnake.Member=None):
        if member is None or member == ctx.author:
            target = "themselves"
            db_target = "SELF"
            member = ctx.author
        else:
            target = member.mention
            db_target = "OTHER"

        gifs = os.listdir(f"./RP/nom/")
        if gifs == []:
            return

        rnd_gif = choice(gifs)

        while rnd_gif == self.nom_last:
            rnd_gif = choice(gifs)
        
        path_to_gif = f"./RP/nom/{rnd_gif}"
        file = disnake.File(path_to_gif, filename="gif.gif")

        kiss_embed = disnake.Embed(
            title="",
            description=f"{ctx.author.mention} took a bite of {target}",
        )
        kiss_embed.set_image(url="attachment://gif.gif")

        rp_db = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).get().val()
        if rp_db == None:
            db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).set(1)
        elif rp_db != None:
            p = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).get().val() + 1
            db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).set(p)
        else:
            await ctx.send("Rarest error ever, please contact developer!!!")

        self_num = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child("SELF").get().val()
        other_num = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child("OTHER").get().val()

        if other_num == None:
            other_time = "times"
            other_num = 0
        elif other_num > 1:
            other_time = "times"
        else:
            other_time = "time"
            
        if self_num == None:
            self_time = "times"
            self_num = 0
        elif self_num > 1:
            self_time = "times"
        else:
            self_time = "time"

        kiss_embed.set_footer(text=f"Others: {other_num} {other_time}\nThemselves: {self_num} {self_time}")
        self.nom_last = rnd_gif
        await ctx.send(embed=kiss_embed, file=file)

    @commands.command(pass_context=True)
    async def pat(self, ctx, member:disnake.Member=None):
        if member is None or member == ctx.author:
            target = "themselves"
            db_target = "SELF"
            member = ctx.author
        else:
            target = member.mention
            db_target = "OTHER"

        gifs = os.listdir(f"./RP/pat/")
        if gifs == []:
            return

        rnd_gif = choice(gifs)

        while rnd_gif == self.pat_last:
            rnd_gif = choice(gifs)
        
        path_to_gif = f"./RP/pat/{rnd_gif}"
        file = disnake.File(path_to_gif, filename="gif.gif")

        kiss_embed = disnake.Embed(
            title="",
            description=f"{ctx.author.mention} patted {target}",
        )
        kiss_embed.set_image(url="attachment://gif.gif")

        rp_db = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).get().val()
        if rp_db == None:
            db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).set(1)
        elif rp_db != None:
            p = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).get().val() + 1
            db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).set(p)
        else:
            await ctx.send("Rarest error ever, please contact developer!!!")

        self_num = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child("SELF").get().val()
        other_num = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child("OTHER").get().val()

        if other_num == None:
            other_time = "times"
            other_num = 0
        elif other_num > 1:
            other_time = "times"
        else:
            other_time = "time"
            
        if self_num == None:
            self_time = "times"
            self_num = 0
        elif self_num > 1:
            self_time = "times"
        else:
            self_time = "time"

        kiss_embed.set_footer(text=f"Others: {other_num} {other_time}\nThemselves: {self_num} {self_time}")
        self.pat_last = rnd_gif
        await ctx.send(embed=kiss_embed, file=file)

    @commands.command(pass_context=True)
    async def punch(self, ctx, member:disnake.Member=None):
        if member is None or member == ctx.author:
            target = "themselves"
            db_target = "SELF"
            member = ctx.author
        else:
            target = member.mention
            db_target = "OTHER"

        gifs = os.listdir(f"./RP/punch/")
        if gifs == []:
            return

        rnd_gif = choice(gifs)

        while rnd_gif == self.punch_last:
            rnd_gif = choice(gifs)
        
        path_to_gif = f"./RP/punch/{rnd_gif}"
        file = disnake.File(path_to_gif, filename="gif.gif")

        kiss_embed = disnake.Embed(
            title="",
            description=f"{ctx.author.mention} punched {target}",
        )
        kiss_embed.set_image(url="attachment://gif.gif")

        rp_db = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).get().val()
        if rp_db == None:
            db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).set(1)
        elif rp_db != None:
            p = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).get().val() + 1
            db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).set(p)
        else:
            await ctx.send("Rarest error ever, please contact developer!!!")

        self_num = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child("SELF").get().val()
        other_num = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child("OTHER").get().val()

        if other_num == None:
            other_time = "times"
            other_num = 0
        elif other_num > 1:
            other_time = "times"
        else:
            other_time = "time"
            
        if self_num == None:
            self_time = "times"
            self_num = 0
        elif self_num > 1:
            self_time = "times"
        else:
            self_time = "time"

        kiss_embed.set_footer(text=f"Others: {other_num} {other_time}\nThemselves: {self_num} {self_time}")
        self.punch_last = rnd_gif
        await ctx.send(embed=kiss_embed, file=file)

    @commands.command(pass_context=True)
    async def slap(self, ctx, member:disnake.Member=None):
        if member is None or member == ctx.author:
            target = "themselves"
            db_target = "SELF"
            member = ctx.author
        else:
            target = member.mention
            db_target = "OTHER"

        gifs = os.listdir(f"./RP/slap/")
        if gifs == []:
            return

        rnd_gif = choice(gifs)

        while rnd_gif == self.slap_last:
            rnd_gif = choice(gifs)
        
        path_to_gif = f"./RP/slap/{rnd_gif}"
        file = disnake.File(path_to_gif, filename="gif.gif")

        kiss_embed = disnake.Embed(
            title="",
            description=f"{ctx.author.mention} slapped {target}",
        )
        kiss_embed.set_image(url="attachment://gif.gif")

        rp_db = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).get().val()
        if rp_db == None:
            db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).set(1)
        elif rp_db != None:
            p = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).get().val() + 1
            db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).set(p)
        else:
            await ctx.send("Rarest error ever, please contact developer!!!")

        self_num = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child("SELF").get().val()
        other_num = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child("OTHER").get().val()

        if other_num == None:
            other_time = "times"
            other_num = 0
        elif other_num > 1:
            other_time = "times"
        else:
            other_time = "time"
            
        if self_num == None:
            self_time = "times"
            self_num = 0
        elif self_num > 1:
            self_time = "times"
        else:
            self_time = "time"

        kiss_embed.set_footer(text=f"Others: {other_num} {other_time}\nThemselves: {self_num} {self_time}")
        self.slap_last = rnd_gif
        await ctx.send(embed=kiss_embed, file=file)

    @commands.command(pass_context=True)
    async def smile(self, ctx, member:disnake.Member=None):
        if member is None or member == ctx.author:
            target = "themselves"
            db_target = "SELF"
            member = ctx.author
        else:
            target = member.mention
            db_target = "OTHER"

        gifs = os.listdir(f"./RP/smile/")
        if gifs == []:
            return

        rnd_gif = choice(self.gifs)

        while rnd_gif == self.smile_last:
            rnd_gif = choice(self.gifs)
        
        path_to_gif = f"./RP/smile/{rnd_gif}"
        file = disnake.File(path_to_gif, filename="gif.gif")

        kiss_embed = disnake.Embed(
            title="",
            description=f"{ctx.author.mention} smiled at {target}",
        )
        kiss_embed.set_image(url="attachment://gif.gif")

        rp_db = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).get().val()
        if rp_db == None:
            db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).set(1)
        elif rp_db != None:
            p = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).get().val() + 1
            db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child(db_target).set(p)
        else:
            await ctx.send("Rarest error ever, please contact developer!!!")

        self_num = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child("SELF").get().val()
        other_num = db.child("COUNTERS").child("RP").child(ctx.guild.id).child(ctx.author.id).child(ctx.command.name).child("OTHER").get().val()

        if other_num == None:
            other_time = "times"
            other_num = 0
        elif other_num > 1:
            other_time = "times"
        else:
            other_time = "time"
            
        if self_num == None:
            self_time = "times"
            self_num = 0
        elif self_num > 1:
            self_time = "times"
        else:
            self_time = "time"

        kiss_embed.set_footer(text=f"Others: {other_num} {other_time}\nThemselves: {self_num} {self_time}")
        self.smile_last = rnd_gif
        await ctx.send(embed=kiss_embed, file=file)

def setup(client):
    client.add_cog(Roleplay(client))