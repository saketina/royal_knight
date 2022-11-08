import PIL
from PIL import Image, ImageDraw, ImageFont
import os
import random


class WelcomeImage:
    def __init__(self, member):
        self.member = member
        self.images_dir = '/'  # 'cogs/Assets/welcome/images/'
        self.images = os.listdir()  # self.images_dir
        self.welcome_image = Image
        self.font = ImageFont.truetype('../good-times.regular.ttf', size=40)

    def PickImage(self):
        random_image = random.choice(self.images)
        # return os.path.join(self.images_dir, random_image)
        return random_image

    def CreateImage(self, path):
        self.welcome_image = Image.open(self.PickImage())
        output_image = self.welcome_image
        draw_cur = ImageDraw.Draw(output_image)
        draw_cur.text((100, 70), "Welcome to the Server!", fill=(
            0, 0, 0, 255), font=self.font, stroke_width=1)
        output_image.save(path)


wew_variable = WelcomeImage("nothing")
wew_variable.CreateImage("output/test.png")
