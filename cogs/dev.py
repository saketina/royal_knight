import json

import disnake
import pyrebase
from disnake.ext import commands
from disnake.ext.commands import is_owner

## make cmd dev only

firebase = pyrebase.initialize_app(
    json.load(open("firebase_config.json", "r")))
db = firebase.database()


class Utility(commands.Cog):
    def __init__(self, client):
        self.client = client

    
    @commands.command()
    async def delwarns(self, ctx, member:disnake.Member=None):
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

    @commands.command(pass_context=True)
    #@has_permissions(administrator=True)
    async def status(self, ctx, activity=None, *, text=None):
        if activity == "playing":
            act = disnake.Activity(type=disnake.ActivityType.playing, name=text)
            response = "Playing"
            await self.client.change_presence(activity=act, status=disnake.Status.dnd)
            await ctx.send(f"Status changed to `{response} {text}`")

        elif activity == "streaming":
            act = disnake.Activity(type=disnake.ActivityType.streaming, name=text)
            response = "Streaming"
            await self.client.change_presence(activity=act, status=disnake.Status.dnd)
            await ctx.send(f"Status changed to `{response} {text}`")

        elif activity == "watching":
            act = disnake.Activity(type=disnake.ActivityType.watching, name=text)
            response = "Watching"
            await self.client.change_presence(activity=act, status=disnake.Status.dnd)
            await ctx.send(f"Status changed to `{response} {text}`")

        elif activity == "competing":
            act = disnake.Activity(type=disnake.ActivityType.competing, name=text)
            response = "Competing in"
            await self.client.change_presence(activity=act, status=disnake.Status.dnd)
            await ctx.send(f"Status changed to `{response} {text}`")

        elif activity == "remove":
            act = disnake.Activity(type=disnake.ActivityType.custom, name=None)
            await self.client.change_presence(activity=act, status=disnake.Status.dnd)
            await ctx.send(f"Status changed to `{text}`")

        elif activity==None or text==None:
            embed = disnake.Embed(
            title="STATUS HELP",
            description="``k.status [activity] [text]``",
            color = disnake.Color.dark_red()
            )
            embed.add_field(
            name="Activity",
            value="playing" + "\n" +
                  "streaming" + "\n" +
                  "watching" + "\n" +
                  "competing" + "\n" +
                  "remove"
            )

            await ctx.send(embed=embed)
        else:
            await ctx.send("I didn\'t quite catch that.")

    @commands.command(pass_context=True)
    async def say(self, ctx, *, message):
        if message != None:
             
            if str(ctx.guild.default_role) not in message and "@here" not in message:
                msg = message
            else:
                msg = "You can\'t make me say that"
            
            await ctx.message.delete()
            await ctx.send(msg)
        else: 
            await ctx.send("Please tell me what to say")

        
    @commands.command(name='eval', pass_context=True)
    @commands.is_owner()
    async def eval_command(self, ctx, *, expr):
        try:
            if 'await ' in expr:
                new_expr = expr.replace('await ', '')
                ans = await eval(new_expr)
            else:
                ans = eval(expr)
            await ctx.send(f"Answer: {ans}")
        except Exception as e:
            print(e.__traceback__)
            await ctx.send("Didn't work.")

    @commands.command(name="toggle", pass_context=True)
    @commands.is_owner()
    async def toggle(self, ctx, *, command):
        command = self.client.get_command(command)

        if command is None:
            embed = disnake.Embed(title="ERROR", description="I can't find a command with that name!", color=0xff0000)
            await ctx.send(embed=embed)

        elif ctx.command == command:
            embed = disnake.Embed(title="ERROR", description="You cannot disable this command.", color=0xff0000)
            await ctx.send(embed=embed)

        else:
            command.enabled = not command.enabled
            ternary = "enabled" if command.enabled else "disabled"
            embed = disnake.Embed(title="Toggle", description=f"I have {ternary} {command.qualified_name} for you!", color=0xff00c8)
            await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def leave(self, ctx, *, guildinput):
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

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def servers(self, ctx):
        await ctx.send(f"{len(self.client.guilds)}")
        listofids = []
        for guild in self.client.guilds:
            listofids.append(guild.id)
        await ctx.send(listofids)

def setup(client):
    client.add_cog(Dev(client))
    print(f"Cog: Dev - loaded.")

def teardown(client):
    print(f"Cog: Dev - unloaded.")
