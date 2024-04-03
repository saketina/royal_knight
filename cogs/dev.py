import json
import os
import platform

import disnake
import psutil
import pyrebase
from disnake.ext import commands
from disnake.ext.commands import is_owner

## make cmd dev only

firebase = pyrebase.initialize_app(
    json.load(open("./firebase_config.json", "r")))
db = firebase.database()


class Dev(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def cls(self, ctx):
        try:
            os.system("cls")
            await ctx.send("Cleared the terminal, Daddy.")
        except commands.NotOwner:
            return
        except Exception as e:
            print(f"Error: \nType: {type(e).__name__} \nInfo - {e}")

    @commands.command()
    @commands.is_owner()
    async def system_info(self, ctx):
        # Get system information
        system_info = {
            "Operating System": platform.system(),
            "Release Version": platform.release(),
            "CPU Usage": f"{psutil.cpu_percent()}%",
            "RAM Usage": f"{psutil.virtual_memory().percent}%",
            "Disk Usage": f"{psutil.disk_usage('/').percent}%",
        }

        # Create an embed to display the information
        embed = disnake.Embed(title="System Information", color=disnake.Color.blue())

        for key, value in system_info.items():
            embed.add_field(name=key, value=value, inline=False)

        await ctx.send(embed=embed)

    
    @commands.command()
    @commands.is_owner()
    async def delmods(self, ctx, member:disnake.Member=None):
        try:
            if member != None:
                try:
                    db_warns = db.child("MODERATIONS").child("WARNS").child(ctx.guild.id).child(member.id).get().val()
                    if db_warns != None:
                        button_yes = Button(label="Yes", style=disnake.ButtonStyle.green)
                        button_no = Button(label="No", style=disnake.ButtonStyle.red)

                        async def button_yes_callback(interaction):
                            if interaction.author.id == ctx.author.id:
                                db.child("MODERATIONS").child("WARNS").child(ctx.guild.id).child(member.id).remove()
                                await interaction.response.edit_message(content="All warns have been deleted", view=None)
                            else:
                                return

                        async def button_no_callback(interaction):
                            if interaction.author.id == ctx.author.id:
                                await interaction.response.edit_message(content="I didn\'t delete any warn", view=None)
                            else:
                                return

                        button_yes.callback = button_yes_callback
                        button_no.callback = button_no_callback

                        view = View(timeout=30)
                        view.add_item(button_yes)
                        view.add_item(button_no)
                        msg = await ctx.send("Are you sure?", view=view)


                    else:
                        await ctx.send("There aren\'t any moderations to delete")
                except:
                    await ctx.send("There was an error. Please contact the dev.")
            else:
                await ctx.send("Please input a member.")
        except commands.NotOwner:
            return
        except Exception as e:
            print(f"Error: \nType: {type(e).__name__} \nInfo - {e}")

    
        
    @commands.command(name='eval', pass_context=True)
    @commands.is_owner()
    async def eval(self, ctx, *, expr):
        try:
            if 'await ' in expr:
                new_expr = expr.replace('await ', '')
                ans = await eval(new_expr)
            else:
                ans = eval(expr)
            await ctx.send(f"Answer: {ans}")
        except commands.NotOwner:
            return
        except Exception as e:
            raise e
            await ctx.send("Didn't work.")

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def leave(self, ctx, *, guildinput):
        try:
            try:
                guildid = int(guildinput)
            except:
                await ctx.send("Invalid guild: failed to convert to int")

            try:
                guild = self.client.get_guild(guildid)
            except:
                await ctx.send("Invalid guild")

            try:
                await guild.leave()
                await ctx.send(f"left {guild.name}")
            except:
                await ctx.send("Error leaving")
        except commands.NotOwner:
            return
        except Exception as e:
            print(f"Error: \nType: {type(e).__name__} \nInfo - {e}")

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def servers(self, ctx):
        try:
            await ctx.send(f"{len(self.client.guilds)}")
            listofids = []
            for guild in self.client.guilds:
                listofids.append(guild.id)
            await ctx.send(listofids)
        except commands.NotOwner:
            return
        except Exception as e:
            print(f"Error: \nType: {type(e).__name__} \nInfo - {e}")

def setup(client):
    client.add_cog(Dev(client))
    print(f"Cog: Dev - loaded.")

def teardown(client):
    print(f"Cog: Dev - unloaded.")
