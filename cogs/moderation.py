import disnake
from disnake.ext import commands
from disnake.ext.commands import has_permissions

from disnake.ui import Button, View

import datetime
from datetime import datetime as dt

import pyrebase
import json

firebase = pyrebase.initialize_app(json.load(open("firebase_config.json", "r")))
db = firebase.database()

dt_string = dt.now().strftime("%d/%m/%Y %H:%M:%S")

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.guild_only()
    async def warn(self, ctx, member:disnake.Member=None, *, reason:str=None):
        if member == None:
            embed = disnake.Embed(
                title = "WARN COMMAND",
                description = "``k.warn [member_id/@member] [reason]``",
                color = disnake.Color.dark_red()
                )
            await ctx.send(embed=embed)
        elif reason == None:
            await ctx.send("Please give me a reason.")
        elif member.id == self.client.user.id:
            await ctx.send("Please don\'t warn me.")
        elif member == ctx.author:
            await ctx.send("You can\'t warn yourself.")
        elif member.guild_permissions.manage_messages == True:
            await ctx.send("You can\'t warn that user.")
        else:
            f = db.child("MODERATIONS").child("WARNS").child(ctx.guild.id).child(member.id).get().val()
            data = f
            if data == None:
                wrn_amount = 1
                data = ({
                    "warns": 1,
                    1:({
                        "moderator": str(ctx.author.id),
                        "moderator_name": str(ctx.author.display_name),
                        "reason": reason,
                        "datetime": dt_string
                    })
                })
                db.child("MODERATIONS").child("WARNS").child(ctx.guild.id).child(member.id).set(data)
                embed = disnake.Embed(
                    title = f"{member.name} has been warned",
                    color = disnake.Color.dark_red()
                    )
                embed.add_field(
                    name = "Warn",
                    value = f"Warn ID: ``{wrn_amount}``\nModerator: **``{ctx.author}``**\nReason: **`{reason}`**\nAt: **``{dt_string}``**",
                    inline = True
                    )
                await ctx.send(embed=embed)
            else:
                wrn_amount = data.get("warns")
                wrn_amount += 1
                data["warns"]=wrn_amount
                new_warn = ({
                    "moderator": str(ctx.author.id),
                    "moderator_name": str(ctx.author.display_name),
                    "reason": reason,
                    "datetime": dt_string
                })
                data[wrn_amount]=new_warn
                db.child("MODERATIONS").child("WARNS").child(ctx.guild.id).child(member.id).set(data)

                embed = disnake.Embed(
                    title = f"{member.name} has been warned",
                    color = disnake.Color.dark_red()
                )
                embed.add_field(
                    name = f"New Warn",
                    value = f"Warn ID: ``{wrn_amount}``\nModerator: **``{ctx.author}``**\nReason: **`{reason}`**\nAt: **``{dt_string}``**"
                )
                await ctx.send(embed=embed)

    @commands.command()
    async def count(self, ctx, user:disnake.User=None):
        db_warns = db.child(
        "MODERATIONS").child(
        "WARNS").child(
        ctx.guild.id).child(
        user.id).get().val()
        warn_count = len(db_warns) - 1
        warn_number = 1
        warn = db_warns.get("1")
        #warn = list(wrn)

        date = warn.get("datetime")
        moderator = warn.get("moderator")
        mod_name = warn.get("moderator_name")
        reason = warn.get("reason")

        warns_embed = disnake.Embed(
            title = f"{user.name}\'s Warnings",
            color = disnake.Color.dark_red()
        )
        warns_embed.add_field(
            name = f"{warn_number}/{warn_count}",
            value = f"Moderator: `{mod_name}`\nModerator ping: <@!{moderator}>\nReason: `{reason}`\nAt: `{date}`"
        )
        await ctx.send(embed=warns_embed)

    @warn.error
    async def warn_handler(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            return
        elif isinstance(error, commands.MissingPermissions):
            return
        else:
            print(error)

    @commands.command()
    async def delwarns(self, ctx, member:disnake.Member=None):
        if member != None:
            try:
                db_warns = db.child("MODERATIONS").child("WARNS").child(ctx.guild.id).child(member.id).get().val()
                if db_warns != None:
                    button_yes = Button(label="Yes", style=disnake.ButtonStyle.green)
                    button_no = Button(label="No", style=disnake.ButtonStyle.red)

                    async def button_yes_callback(interaction):
                        db.child("MODERATIONS").child("WARNS").child(ctx.guild.id).child(member.id).remove()
                        await interaction.response.edit_message(content="All warns have been deleted", view=None)

                    async def button_no_callback(interaction):
                        await interaction.response.edit_message(content="I didn\'t delete any warn", view=None)

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
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount:int=None):
        if amount==None:
            emb = disnake.Embed(
                title = "PURGE HELP",
                description = "`k.purge [amount]`",
                color = disnake.Color.dark_red()
                )
            await ctx.send(embed=emb)
        elif amount==0:
            msg = await ctx.send("Please input a number larger then 0.")
            await msg.delete(delay=10)

        elif amount<1001:
            if amount>1:
                msgs = "messages"
            else:
                msgs = "message"

            deleted = await ctx.channel.purge(limit = amount, bulk=True)
            msg = await ctx.send(f"Successfully deleted {len(deleted)} {msgs}.")
            await msg.delete(delay=10)
        else:
            await ctx.send("You can\'t delete more then 1000 messages at a time.")

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            return
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("I didn\'t quite catch that.")
        elif isinstance(error, commands.BadArgument):
            msg = await ctx.send("Please input only numbers.")
            await msg.delete(delay=10)
        elif isinstance(error, commands.MissingPermissions):
            return
        else:
            print(error)

    @commands.command(pass_context=True)
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member:disnake.User=None, *, reason=None):
        if member==None:
            emb = disnake.Embed(
                title = "BAN HELP",
                description = "`k.ban [mention/user_id] (reason)`",
                color = disnake.Color.dark_red()
                )
            await ctx.send(embed=emb)
        elif member==ctx.author:
            msg = await ctx.send("You can\'t ban yourself")
            await msg.delete(delay=10)
        else:
            if reason==None:
                rsn="no reason"
            else:
                rsn=reason

            f = db.child("MODERATIONS").child("BANS").child(ctx.guild.id).child(member.id).get().val()
            data = f
            if data == None:
                data = ({
                    "bans": 1,
                    1:({
                        "moderator": str(ctx.author.id),
                        "moderator_name": str(ctx.author.name),
                        "reason": reason,
                        "datetime": dt_string
                    })
                })
                db.child("MODERATIONS").child("BANS").child(ctx.guild.id).child(member.id).set(data)
                embed = disnake.Embed(
                    title = f"{member.name} has been banned.",
                    color = disnake.Color.dark_red()
                    )
                embed.add_field(
                    name = "Ban",
                    value = f"Moderator: {ctx.author}\nReason: `{reason}`\nAt: {dt_string}",
                    inline = True
                    )
                await ctx.send(embed=embed)
            else:
                bn_amount = data.get("bans")
                bn_amount += 1
                data["bans"]=bn_amount
                new_ban = ({
                    "moderator": str(ctx.author.id),
                    "moderator_name": str(ctx.author.name),
                    "reason": reason,
                    "datetime": dt_string
                })
                data[bn_amount]=new_ban
                db.child("MODERATIONS").child("BANS").child(ctx.guild.id).child(member.id).set(data)

                embed = disnake.Embed(
                    title = f"{member.name} has been banned.",
                    color = disnake.Color.dark_red()
                )
                embed.add_field(
                    name = f"Ban {bn_amount}",
                    value = f"Moderator: {ctx.author}\nReason: `{reason}`\nAt: {dt_string}"
                )
                await ctx.send(embed=embed)
            await ctx.guild.ban(member, reason=f"By {ctx.author} was banned for {rsn}.")
            #await ctx.send(f"{member} was banned for {rsn}.")

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            return
        elif isinstance(error, commands.MemberNotFound):
            msg = await ctx.send("I couldn\'t find that member")
            await msg.delete(delay=10)
        elif isinstance(error, commands.MissingPermissions):
            return
        else:
            print(error)

    @commands.command(pass_context=True)
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member:disnake.Member=None, *, reason=None):
        if member==None:
            emb = disnake.Embed(
                title = "KICK HELP",
                description = "`k.kick [mention/user_id] (reason)`",
                color = disnake.Color.dark_red()
                )
            await ctx.send(embed=emb)
        elif member==ctx.author:
            msg = await ctx.send("You can\'t kick yourself")
            await msg.delete(delay=10)
        else:
            if reason==None:
                rsn="no reason"
            else:
                rsn=reason

            f = db.child("MODERATIONS").child("KICKS").child(ctx.guild.id).child(member.id).get().val()
            data = f
            if data == None:
                data = ({
                    "kicks": 1,
                    1:({
                        "moderator": str(ctx.author.id),
                        "moderator_name": str(ctx.author.name),
                        "reason": reason,
                        "datetime": dt_string
                    })
                })
                db.child("MODERATIONS").child("KICKS").child(ctx.guild.id).child(member.id).set(data)
                embed = disnake.Embed(
                    title = f"{member.name} has been kicked",
                    color = disnake.Color.dark_red()
                    )
                embed.add_field(
                    name = "Kick",
                    value = f"Moderator: {ctx.author}\nReason: `{reason}`\nAt: {dt_string}",
                    inline = True
                    )
                await ctx.send(embed=embed)
            else:
                kck_amount = data.get("kicks")
                kck_amount += 1
                data["kicks"]=kck_amount
                new_kick = ({
                    "moderator": str(ctx.author.id),
                    "moderator_name": str(ctx.author.name),
                    "reason": reason,
                    "datetime": dt_string
                })
                data[kck_amount]=new_kick
                db.child("MODERATIONS").child("KICKS").child(ctx.guild.id).child(member.id).set(data)

                embed = disnake.Embed(
                    title = f"{member.name} has been kicked",
                    color = disnake.Color.dark_red()
                )
                embed.add_field(
                    name = f"Ban {kck_amount}",
                    value = f"Moderator: {ctx.author}\nReason: `{reason}`\nAt: {dt_string}"
                )
                await ctx.send(embed=embed)
            await ctx.guild.kick(member, reason=f"By {ctx.author} was kicked for {rsn}.")
            #await ctx.send(f"{member} was kicked for {rsn}.")

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            return
        elif isinstance(error, commands.MemberNotFound):
            msg = await ctx.send("I couldn\'t find that member")
            await msg.delete(delay=10)
        if isinstance(error, commands.MissingPermissions):
            return
        else:
            print(error)

    @commands.command(pass_context=True)
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, id: int = None):
        if id == None:
            emb = disnake.Embed(
                title = "UNBAN HELP",
                description = "`k.unban [user_id]`",
                color = disnake.Color.dark_red()
                )
            await ctx.send(embed=emb)
        elif id == ctx.author:
            msg = await ctx.send("You aren\'t banned.")
            await msg.delete(delay=10)
        else:
            user = await self.client.fetch_user(id)
            await ctx.guild.unban(user)
            await ctx.send(f"{user} has been unbanned.")

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            return
        elif isinstance(error, commands.BadArgument):
            msg = await ctx.send("Please input only the members id.")
            await msg.delete(delay=10)
        elif isinstance(error, commands.CommandInvokeError):
            msg = await ctx.send("I can\'t find that member.")
            await msg.delete(delay=10)
        elif isinstance(error, commands.MissingPermissions):
            msg = await ctx.send("You don\'t have the required permissions to use this command.")
            await msg.delete(delay=10)
        else:
            print(error)

def setup(client):
    client.add_cog(Moderation(client))
    print(f"Cog: Moderation - loaded.")

def teardown(client):
    print(f"Cog: Moderation - unloaded.")