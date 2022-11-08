import numpy as np
from PIL import Image, ImageDraw, ImageOps, ImageFont
import os
from io import BytesIO
import requests
from random import choice

PFP_URL = "https://cdn.discordapp.com/avatars/666578281142812673/6646218f8b759da4a8f688aeef4eb2c2.png?size=256"
r = requests.get(PFP_URL)
img = Image.open(BytesIO(r.content))
mask = Image.open("mask.png").convert("L")
output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
output.putalpha(mask)

# output.show()

images_dir = "./cogs/Assets/welcome/images/welcome_image/"
images = [image for image in os.listdir(images_dir) if image[-4:] == ".png"]
random_image = os.path.join(images_dir, choice(images))


im = Image.open(random_image)
output = output.resize((im.height - 10, im.height - 10))  # height of background
im.paste(output, (6, 6), output)

font_big = ImageFont.truetype("./cogs/Assets/welcome/ZenDots-Regular.ttf", 60)
font_smol = ImageFont.truetype("./cogs/Assets/welcome/ZenDots-Regular.ttf", 55)
draw_cur = ImageDraw.Draw(im)
draw_cur.text(
    (260, 60),
    "Welcome to the Server!",
    fill=(115, 115, 250, 255),
    stroke_width=3,
    font=font_big,
    stroke_fill=(0, 0, 100, 255),
)
draw_cur.text(
    (260, 130),
    f"weeblet~kun#0039",
    fill=(224, 122, 255, 255),
    stroke_width=3,
    stroke_fill=(0, 0, 0, 255),
    font=font_smol,
)


im.show()
