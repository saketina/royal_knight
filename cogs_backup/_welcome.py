import disnake
from disnake.ext import commands

from datetime import datetime
import random
import PIL
from PIL import Image, ImageFont, ImageDraw
import os
import requests
from io import BytesIO


class WelcomeImage:
    def __init__(self, member):
        self.member = member
        self.images_dir = "./cogs/Assets/welcome/images/welcome_image/"
        self.images = [
            image for image in os.listdir(self.images_dir) if image[-4:] == ".png"
        ]
        self.welcome_image = Image
        self.font1 = ImageFont.truetype(
            f"cogs/Assets/welcome/good-times.regular.ttf", size=50
        )
        self.font2 = ImageFont.truetype(
            f"cogs/Assets/welcome/good-times.regular.ttf", size=60
        )
        self.output_image_path = (
            self.images_dir + "output/" + str(self.member.id) + ".png"
        )

    def PickImage(self):
        random_image = random.choice(self.images)
        return os.path.join(self.images_dir, random_image)
        # return random_image

    def CreateImage(self):
        picked_image = self.PickImage()
        self.welcome_image = Image.open(picked_image)
        output_image = self.welcome_image
        draw_cur = ImageDraw.Draw(output_image)
        draw_cur.text(
            (50, 50),
            "Welcome to the Server!",
            fill=(0, 0, 0, 255),
            font=self.font1,
            stroke_width=1,
            stroke_fill=(255, 255, 255, 255),
        )
        draw_cur.text(
            (260, 130),
            f"{self.member.name}#{self.member.discriminator}",
            fill=(224, 122, 255, 255),
            font=self.font2,
            stroke_width=3,
            stroke_fill=(0, 0, 0, 255),
        )
        mem_display_avatar = requests.get(self.member.display_avatar)
        av_img = Image.open(BytesIO(mem_display_avatar.content)).resize((200, 200))
        output_image.paste(av_img, (50, 120))
        output_image.save(self.output_image_path)


class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.welcome_images = [
            "https://www.pngkit.com/png/detail/124-1244996_transparent-welcome-anima-image-royalty-free-download-anime.png",
            "https://cdn140.picsart.com/286390297028201.png?type=webp&to=min&r=640",
            "https://media1.tenor.com/images/a03b5e72efa1834796814ae85c98151b/tenor.gif?itemid=15911925",
            "https://lunasy.org/wp-content/uploads/2017/02/16830618_1872079239727924_6150302759558259434_n.jpg",
            "https://animeforums.net/uploads/monthly_2019_07/welcome.jpeg.808b153eb9114668d40492e1ea22a6ba.jpeg",
            "https://media1.tenor.com/images/068081ee5b913a47003a64f7233825fe/tenor.gif?itemid=14815902",
        ]

    """
    OLD WELCOME MESSAGE

    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcome_channel = await self.client.fetch_channel(669509495965351938)
        member_count = member.guild.member_count
        end_letter = ''
        if member_count%10 == 1:
            end_letter='st'
        elif member_count%10 == 2:
            end_letter = 'nd'
        elif member_count%10 == 3:
            end_letter = 'rd'
        else:
            end_letter = 'th'
        welcome_embed = discord.Embed(
            title=f'Welcome to Royal Weebs',
            description=f"**Konichiwa {member.mention}\nYou're our {member_count}{end_letter} member!**"
                        f"Things you might have to do:\n1. Please be sure to read <#687013558352871430>,\n"
                        f"2. Grab some free roles from <#695213724478472238>"
                        f"**Thanks for joining!!**",
            color=discord.Color.green(),
            timestamp=datetime.utcnow(),
        )
        welcome_embed.set_author(name=f'Royal Weebs', icon_url=f'{member.guild.icon_url}')
        welcome_embed.set_thumbnail(url=member.display_avatar)
        welcome_embed.set_image(url=random.choice(self.welcome_images))
        welcome_embed.set_footer(text='Joined at | ')

        await welcome_channel.send(embed=welcome_embed)
        """

    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcome_channel = await self.client.fetch_channel(706011974118408243)
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

        image = WelcomeImage(member)
        await self.client.loop.run_in_executor(None, image.CreateImage)
        image_file = discord.File(image.output_image_path)
        await welcome_channel.send(
            f"Welcome {member.mention}, You're our {member_count}{end_letter} member, "
            f"don’t forget to read <#687013558352871430> "
            f"and check <#695213724478472238>",
            file=image_file,
        )


def setup(client):
    client.add_cog(Welcome(client))
