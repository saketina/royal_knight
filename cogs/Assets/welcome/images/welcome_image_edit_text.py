import PIL
from PIL import Image, ImageDraw, ImageFont
import os
import random


class WelcomeImage:
    def __init__(self, member):
        self.member = member
        self.images_dir = './welcome_image'  # 'cogs/Assets/welcome/images/new/'
        self.images = os.listdir(self.images_dir)  # self.images_dir
        if ".DS_Store" in self.images:
            self.images.remove(".DS_Store")
        self.welcome_image = Image
        self.font = ImageFont.truetype('../good-times.regular.ttf', size=40)

    def PickImage(self):
        random_image = random.choice(self.images)
        return os.path.join(self.images_dir, random_image)
        # return random_image

    def CreateImage(self, path):
        self.welcome_image = Image.open(self.PickImage())
        output_image = self.welcome_image
        draw_cur = ImageDraw.Draw(output_image)
        draw_cur.text((50, 50), "Welcome to the Server!", fill=(
            0, 0, 0, 255), font=self.font, stroke_width=1)
        output_image.save(path)


wew_variable = WelcomeImage("nothing")
wew_variable.CreateImage("welcome_image/output/test.png")