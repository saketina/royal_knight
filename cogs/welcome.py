import os
import random
from datetime import datetime
from io import BytesIO
from random import choice

import disnake
import PIL
import requests
from disnake.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageOps

import logging

logging = logging.getLogger("Welcome")

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == 940292707102900244:  # TESTING SERVER
            welcome_channel = await self.bot.fetch_channel(
                960371515759689788
            )  # TS welcome
            server = "Testing Server"
        else:
            return

        member_count = member.guild.member_count
        end_letter = ""

        if member_count % 10 == 1 and member_count != 11:
            end_letter = "st"

        elif member_count % 10 == 2 and member_count != 12:
            end_letter = "nd"

        elif member_count % 10 == 3 and member_count != 13:
            end_letter = "rd"

        else:
            end_letter = "th"

        try:
            r = requests.get(member.display_avatar)
            img = Image.open(BytesIO(r.content)).convert("RGBA")
            mask = Image.open("mask.png").convert("L")
            output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
            output.putalpha(mask)

            # output.show()

            images_dir = "cogs/Assets/welcome/images/welcome_image/"
            images = [image for image in os.listdir(images_dir) if image[-4:] == ".png"]
            random_image = os.path.join(images_dir, choice(images))

            im = Image.open(random_image).convert("RGBA")
            output = output.resize(
                (im.height - 10, im.height - 10)
                )  # height of background
            im.paste(output, (6, 6), output)
        except Exception as e:
            await welcome_channel.send(
                f"WELCOME ERROR : {e}\n\n fix this shit <@666578281142812673>, <@385683162799538176>"
                )

        font_big = ImageFont.truetype("cogs/Assets/welcome/ZenDots-Regular.ttf", 60)
        font_smol = ImageFont.truetype("cogs/Assets/welcome/ZenDots-Regular.ttf", 55)
        draw_cur = ImageDraw.Draw(im)
        draw_cur.text(
            (260, 60),
            "Welcome to the Server!",
            fill=(249, 133, 139, 255),
            stroke_width=3,
            font=font_big,
            stroke_fill=(118, 17, 55, 255),
            )

        draw_cur.text(
            (260, 130),
            f"{member}",
            fill=(237, 51, 95, 255),
            stroke_width=3,
            stroke_fill=(118, 17, 55, 255),
            font=font_smol,
            )

        path = f"./cogs/Assets/welcome/images/welcome_image/output/{member.id}.png"
        im.save(path)
        image_file = disnake.File(path)
        await welcome_channel.send(
            f"Welcome {member.mention} to the server **{server}**!\nYou are our ``{member_count}{end_letter}`` member.",
            file=image_file,
            )

        try:
            os.system(f"del /q \"C:\\Users\\User\\Documents\\Discord Projects\\karma-master\\cogs\\Assets\\welcome\\images\\welcome_image\\output\\{member.id}.png\"")
        except:
            os.system(f"rm -rf {path}")

def setup(bot):
    bot.add_cog(Welcome(bot))

