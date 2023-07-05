import datetime
import json
from datetime import datetime as dt

import disnake
import pyrebase
from disnake.ext import commands
from disnake.ext.commands import has_permissions

# //TODO remove unneeded imports and lines of code
# //TODO add feature so its easy to add by role perms for commands
# //TODO use try and except or GEH(global error handler) for errors

firebase = pyrebase.initialize_app(json.load(open("firebase_config.json", "r")))
db = firebase.database()

dt_string = dt.now().strftime("%d/%m/%Y %H:%M:%S")

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
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
                    value = f"Warn ID: ``{wrn_amount}``\n"
                            f"Moderator: {ctx.author.mention}\n"
                            f"Reason: **``{reason}``**\n"
                            f"At: **``{dt_string}``**",
                    inline = True
                    )
                #await ctx.send(embed=embed)
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
                    value = f"Warn ID: ``{wrn_amount}``\n"
                            f"Moderator: {ctx.author.mention}\n"
                            f"Reason: **`{reason}`**\n"
                            f"At: **``{dt_string}``**"
                )
            await ctx.send(embed=embed)

    @warn.error
    async def warn_handler(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            return
        elif isinstance(error, commands.MissingPermissions):
            return
        else:
            print(error)

    @commands.command(pass_context=True)
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount:int=None):
        if amount==None:
            emb = disnake.Embed(
                title = "PURGE COMMAND",
                description = "`k.purge [amount]`",
                color = disnake.Color.dark_red()
                )
            await ctx.send(embed=emb)
        elif amount==0:
            await ctx.send(content = "Please input a number larger then 0.", delete_after = 10)

        elif amount<1001:
            if amount>1:
                msgs = "messages"
            else:
                msgs = "message"

            deleted = await ctx.channel.purge(limit = amount + 1, bulk=True)
            await ctx.send(content = f"Successfully deleted {len(deleted) - 1} {msgs}.", delete_after = 10)
        else:
            await ctx.send("You can\'t delete more then 1000 messages at a time.")

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            return
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("I didn\'t quite catch that.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send(content = "Please input only numbers.", delete_after = 10)
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
        elif member.id == self.client.user.id:
            await ctx.send("Please don\'t ban me.")
        elif member==ctx.author:
            await ctx.send(content = "You can\'t ban yourself", delete_after = 10)
        else:
            if reason==None:
                rsn="no reason"
            else:
                rsn=reason

            f = db.child("MODERATIONS").child("BANS").child(ctx.guild.id).child(member.id).get().val()
            data = f
            if data == None:
                bn_amount = 1
                data = ({
                    "bans": 1,
                    1:({
                        "moderator": str(ctx.author.id),
                        "moderator_name": str(ctx.author.display_name),
                        "reason": rsn,
                        "datetime": dt_string
                    })
                })
                db.child("MODERATIONS").child("BANS").child(ctx.guild.id).child(member.id).set(data)
                embed = disnake.Embed(
                    title = f"{member.name} has been banned.",
                    color = disnake.Color.dark_red()
                    )
                embed.add_field(
                    name = "New Ban",
                    value = f"Ban ID: ``{bn_amount}``\n"
                            f"Moderator: {ctx.author.mention}\n"
                            f"Reason: **``{rsn}``**\n"
                            f"At: **``{dt_string}``**",
                    inline = True
                    )
                #await ctx.send(embed=embed)
            else:
                bn_amount = data.get("bans")
                bn_amount += 1
                data["bans"]=bn_amount
                new_ban = ({
                    "moderator": str(ctx.author.id),
                    "moderator_name": str(ctx.author.display_name),
                    "reason": rsn,
                    "datetime": dt_string
                })
                data[bn_amount]=new_ban
                db.child("MODERATIONS").child("BANS").child(ctx.guild.id).child(member.id).set(data)

                embed = disnake.Embed(
                    title = f"{member.name} has been banned.",
                    color = disnake.Color.dark_red()
                )
                embed.add_field(
                    name = f"New Ban",
                    value = f"Ban ID: ``{bn_amount}``\n"
                            f"Moderator: {ctx.author.mention}\n"
                            f"Reason: **`{rsn}`**\n"
                            f"At: **``{dt_string}``**"
                )
            await ctx.guild.ban(member, reason=f"By {ctx.author} was banned for {rsn}.")
            await ctx.send(embed=embed)
            #await ctx.send(f"{member} was banned for {rsn}.")

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            return
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(content = "I couldn\'t find that member", delete_after = 10)
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
            await ctx.send(content = "You can\'t kick yourself", delete_after = 10)
        else:
            if reason==None:
                rsn="no reason"
            else:
                rsn=reason

            f = db.child("MODERATIONS").child("KICKS").child(ctx.guild.id).child(member.id).get().val()
            data = f
            if data == None:
                kck_amount = 1
                data = ({
                    "kicks": 1,
                    1:({
                        "moderator": str(ctx.author.id),
                        "moderator_name": str(ctx.author.display_name),
                        "reason": rsn,
                        "datetime": dt_string
                    })
                })
                db.child("MODERATIONS").child("KICKS").child(ctx.guild.id).child(member.id).set(data)
                embed = disnake.Embed(
                    title = f"{member.name} has been kicked",
                    color = disnake.Color.dark_red()
                    )
                embed.add_field(
                    name = "New Kick",
                    value = f"Kick ID: ``{kck_amount}``\n"
                            f"Moderator: {ctx.author.mention}\n"
                            f"Reason: **``{rsn}``**\n"
                            f"At: **``{dt_string}``**",
                    inline = True
                    )
                #await ctx.send(embed=embed)
            else:
                kck_amount = data.get("kicks")
                kck_amount += 1
                data["kicks"]=kck_amount
                new_kick = ({
                    "moderator": str(ctx.author.id),
                    "moderator_name": str(ctx.author.display_name),
                    "reason": rsn,
                    "datetime": dt_string
                })
                data[kck_amount]=new_kick
                db.child("MODERATIONS").child("KICKS").child(ctx.guild.id).child(member.id).set(data)

                embed = disnake.Embed(
                    title = f"{member.name} has been kicked",
                    color = disnake.Color.dark_red()
                )
                embed.add_field(
                    name = f"New Kick",
                    value = f"Kick ID: ``{kck_amount}``\n"
                            f"Moderator: {ctx.author.mention}\n"
                            f"Reason: **`{rsn}`**\n"
                            f"At: **``{dt_string}``**"
                )
                #await ctx.send(embed=embed)
            await ctx.guild.kick(member, reason=f"By {ctx.author} was kicked for {rsn}.")
            await ctx.send(embed=embed)
            #await ctx.send(f"{member} was kicked for {rsn}.")

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            return
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(content = "I couldn\'t find that member", delete_after = 10)
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
            await ctx.send(content = "You aren\'t banned.", delete_after = 10)
        else:
            user = await self.client.fetch_user(id)
            await ctx.guild.unban(user)
            await ctx.send(f"{user} has been unbanned.")

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            return
        elif isinstance(error, commands.BadArgument):
            await ctx.send(content = "Please input only the members id.", delete_after = 10)
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send(content = "I can\'t find that member.", delete_after = 10)
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(content = "You don\'t have the required permissions to use this command.", delete_after = 10)
        else:
            print(error)

def setup(client):
    client.add_cog(Moderation(client))
    print(f"Cog: Moderation - loaded.")

def teardown(client):
    print(f"Cog: Moderation - unloaded.")