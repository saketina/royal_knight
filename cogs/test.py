import os
import random
from io import BytesIO
from random import choice

import disnake
from disnake.ext import commands
from PIL import Image

gif_storage={}
sniped_messages = {}

def per_cmd_loader(folder):
    loaded_gifs = {}
    gifs = []
    files = os.listdir(f"./RP/{folder}")
    print(files)
    for file_name in files:
        print("done")
        # Get the full path to the GIF
        #gif_path = os.path.join(root, file_name)

        # Open the GIF using Pillow
        gif_im = Image.open(f"./RP/bite/{file_name}")
        image_byt = BytesIO()
        gif_im.resize((500, 264))
        #gif_image.tobytes()
        gif_im.save(image_byt, format="GIF", save_all=True)
        image_byt.seek(0)

        gifs.append(image_byt)
        #gif_image.close()
                

    loaded_gifs = gifs
    print(loaded_gifs)

    #print(loaded_gifs)
    #print(loaded_gifs)
    print("gifs have been preloaded")
    return loaded_gifs  # Return the dictionary of processed GIFs

class Test(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.rp_last = None
        #self.gifs = {}  # Dictionary to store paths of GIFs

    def send_embed(self, title=None, description=None):
        embed = disnake.Embed(
            title=title,
            description=description,
            color=disnake.Color.dark_red()
        )

    def load_gifs(self, gif_folder):
        loaded_gifs = {}  # Create a dictionary to store paths of GIFs

        # Check if the specified directory exists
        if not os.path.exists(gif_folder):
            return loaded_gifs

        # List all files in the specified directory
        files = os.listdir(gif_folder)

        # Filter only the GIF files
        gif_files = [file for file in files if file.lower().endswith((".gif"))]

        for gif_file in gif_files:
            # Get the full path to the GIF
            gif_path = os.path.join(gif_folder, gif_file)

            # Store the path to the dictionary with the file name as the key
            loaded_gifs[gif_file] = gif_path

        return loaded_gifs  # Return the dictionary of GIF paths

    @commands.command()
    async def gif_load_test(self, ctx, gif_folder):
        # Load GIFs from the specified folder
        self.gifs = self.load_gifs(gif_folder)

        # Check if any GIFs were loaded
        if not self.gifs:
            await ctx.send(f"No GIFs found in the folder '{gif_folder}'.")
        else:
            await ctx.send(f"GIFs loaded from the folder '{gif_folder}'.")

    @commands.command()
    async def send_random_gif(self, ctx):
        # Check if there are any loaded GIFs
        if not self.gifs:
            await ctx.send("No GIFs loaded. Use the `gif_load` command to load GIFs.")
            return

        # Select a random GIF path from the loaded GIFs
        random_gif_filename, random_gif_path = random.choice(list(self.gifs.items()))

        # Create an embed with the GIF as an attachment
        embed = disnake.Embed(title="Random GIF", color=disnake.Color.blue())
        
        # Create a disnake.File from the GIF path
        gif_file = disnake.File(random_gif_path, filename=random_gif_filename)
        
        # Set the image URL to the attachment
        embed.set_image(url=f"attachment://{random_gif_filename}")

        # Send the embed with the GIF as an attachment
        await ctx.send(embed=embed, file=gif_file)

    @commands.command()
    async def send_gif(self, ctx):
        rp = os.listdir("./RP/")
        for command in rp:
            counter = 0
            all_gifs = os.listdir(f"./RP/{command}")
            for g in all_gifs:
                try:
                    if gif_storage != {}:
                        
                        """
                        gif = Image.open(f"./RP_OLD/{command}/{g}")
                        selected_gif = gif.resize((500, 264))
                        #gif_bytes = selected_gif.tobytes()
                        path = f"./RP/{command}/{command}({counter}).gif"
                        selected_gif.save(path, format="GIF", save_all=True)
                        

                        gif_imag = Image.open(f"./RP/{command}/{g}")
                        image_bytes = BytesIO()
                        gif_imag.resize((500, 264))
                        gif_imag.tobytes()
                        gif_imag.save(image_bytes, "GIF", save_all=True)
                        #image_bytes = b.getvalue()
                        #print(image_bytes)
                        image_bytes.seek(0)
                        #print(image_bytes)
                        #path = f"./RP/{command}/{command}({counter}).gif"
                        #image_bytes.save(path, format="GIF", save_all=True)
                        #BytesIO.write(gif_image)
                        """
                        gif = gif_storage[command]
                        print(gif)
                        image_bytes = gif[counter]
                    else:
                        loaded_gifs = per_cmd_loader(command)
                        print(f"loaded gifs in {command}")
                        gif = gif_storage[command] = loaded_gifs
                        print("gifs preloaded in command/bite")
                        image_bytes = gif[counter]
                    file = disnake.File(image_bytes, filename="gif.gif")
                    kiss_embed = disnake.Embed(
                        title="",
                        description=f"done with {g}",
                    )
                    kiss_embed.set_image(url="attachment://gif.gif")
                    #kiss_embed.set_footer(text=f"Others: {other_num} {other_time}\nThemselves: {self_num} {self_time}")
                    await ctx.send(embed=kiss_embed, file=file)
                    counter += 1
                    #gif_image.close()
                except Exception as e:
                    await ctx.send(f"failed at {g}")
                    raise e
            return
            ## BUG: this piece of shit works idk how or why, the gifs are moving but on the original rp cmd the embeds arent moving at all

def setup(bot):
    bot.add_cog(Test(bot))
