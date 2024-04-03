import datetime
import json
from datetime import datetime as dt

import disnake
import pyrebase
from disnake import Forbidden
from disnake.ext import commands

# TODO ALL/add feature so its easy to add by role perms for commands
# TODO ALL/use try and except or GEH(global error handler) for errors

# TODO Add a notes tab for moderations similar to reason

firebase = pyrebase.initialize_app(json.load(open("firebase_config.json", "r")))
db = firebase.database()

dt_string = dt.now().strftime("%d/%m/%Y %H:%M:%S")

ban_roles = 687228928565444800,706540593865556071, 743724904033288293, 706161806426767470, 801614132771160095, 747680315257913384
unban_roles = 687228928565444800, 706540593865556071, 743724904033288293, 706161806426767470, 801614132771160095
kick_roles = 687228928565444800, 706540593865556071, 743724904033288293, 706161806426767470, 801614132771160095, 747680315257913384, 870431101955493999
mute_roles = 687228928565444800, 706540593865556071, 743724904033288293, 706161806426767470, 801614132771160095, 747680315257913384, 870431101955493999
unmute_roles = 687228928565444800, 706540593865556071, 743724904033288293, 706161806426767470, 801614132771160095, 747680315257913384
warn_roles = 687228928565444800, 706540593865556071, 743724904033288293, 706161806426767470, 801614132771160095, 747680315257913384, 870431101955493999

def moderation_check(ctx):
    try:
        if ctx.command.name == "ban":
            for role in ctx.author.roles:
                if role.id in ban_roles:
                    return True

            return False
        elif ctx.command.name == "unban":
            for role in ctx.author.roles:
                if role.id in unban_roles:
                    return True

            return False
        elif ctx.command.name == "kick":
            for role in ctx.author.roles:
                if role.id in kick_roles:
                    return True

            return False
        elif ctx.command.name == "mute":
            for role in ctx.author.roles:
                if role.id in mute_roles:
                    return True

            return False
        elif ctx.command.name == "unmute":
            for role in ctx.author.roles:
                if role.id in unmute_roles:
                    return True

            return False
        elif ctx.command.name == "warn":
            for role in ctx.author.roles:
                if role.id in warn_roles:
                    return True

            return False
        elif ctx.command.name == "purge":
            for role in ctx.author.roles:
                if role.id in warn_roles:
                    return True

            return False
    except AttributeError:
        return



class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    # TODO add checks if roles exist in list(multiple-role-sys)
    # TODO when check is complete store roles unable to process to another list and output them to the user
    @commands.command()
    @commands.guild_only()
    async def role(self, ctx, action=None, command=None, *roles:disnake.Role):
        command_list = ["ban", "unban", "kick", "mute", "unmute", "warn", "purge"]

        if action == "add":
            pass
        elif action == "remove":
            pass
        else:
            return
        if command and roles == None:
            embed = disnake.Embed(
                title = "insert help cmd",
                description = "work in progress...",
                color = disnake.Color.dark_red()
            )
            await ctx.send(embed=embed)
        elif command not in command_list:
            await ctx.send("Command not found...")
        elif action == "add":
            if len(roles) == 1:
                temp = db.child("SETUP").child(ctx.guild.id).child("MODERATION").child(command.lower()).get().val()
                print(temp)
                if temp == None:
                    db.child("SETUP").child(ctx.guild.id).child("MODERATION").child(command.lower()).set(roles[0].id)
                elif roles[0].id == temp:
                    await ctx.send(f"Role already set to {command}.")
                    return
                else:
                    temp.append(roles[0].id)
                    db.child("SETUP").child(ctx.guild.id).child("MODERATION").child(command.lower()).set(temp)
                await ctx.send(f"Roles set to {command}")
            else:
                await ctx.send("started list = multiple")
                temp = []
                for role in roles:
                    temp.append(role.id)
                db.child("SETUP").child(ctx.guild.id).child("MODERATION").child(command.lower()).set(temp)
                await ctx.send(f"Roles set to {command}")
        elif action == "remove":
            f = db.child("SETUP").child(ctx.guild.id).child("MODERATION").child(command.lower()).get().val()
            if f != None:
                for role in roles:
                    f.pop(role.id)
                db.child("SETUP").child(ctx.guild.id).child("MODERATION").child(command.lower()).set(temp)
                await ctx.send(f"Roles removed from {command}")
            else:
                await ctx.send("No roles to remove.")
        else:
            await ctx.send(f"Sum ting wong")

    @commands.command()
    @commands.guild_only()
    @commands.check(moderation_check)
    async def warn(self, ctx, member:disnake.Member=None, *, reason:str=None):
        try:
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
            #elif member.guild_permissions.manage_messages == True:
            #    await ctx.send("You can\'t warn that user.")
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
                            "datetime": dt_string,
                            "proof": ""
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
                        "datetime": dt_string,
                        "proof": ""
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
        except Forbidden:
            await ctx.send("You can\'t moderate on that user.")

    @warn.error
    async def warn_handler(self, ctx, error):
        try:
            if isinstance(error, commands.NoPrivateMessage):
                return
            elif isinstance(error, commands.MissingPermissions):
                return
            elif isinstance(error, commands.CheckFailure):
                return
            else:
                print(error)
        except Exception as e:
            print(f"Error: \nType: {type(e).__name__} \nInfo - {e}")
    
    @commands.command()
    @commands.guild_only()
    @commands.check(moderation_check)
    async def purge(self, ctx, amount:int=None):
        if amount==None:
            emb = disnake.Embed(
                title = "PURGE COMMAND",
                description = "`k.purge [amount]`",
                color = disnake.Color.dark_red()
                )
            await ctx.send(embed=emb)
        elif amount<=0:
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

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(ban_members=True)
    @commands.check(moderation_check)
    # TODO add check if user is banned
    async def ban(self, ctx, member:disnake.User=None, *, reason=None):
        try:
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
                            "datetime": dt_string,
                            "proof": ""
                        })
                    })
                    db.child("MODERATIONS").child("BANS").child(ctx.guild.id).child(member.id).set(data)
                    embed = disnake.Embed(
                        title = f"{member.name} has been banned.",
                        color = disnake.Color.dark_red()
                        )
                    embed.add_field(
                        name = "Ban info",
                        value = f"Moderator: {ctx.author.mention}\n"
                                f"Reason: **``{rsn}``**\n"
                                f"At: **``{dt_string}``**",
                        inline = True
                        )
                else:
                    bn_amount = data.get("bans")
                    bn_amount += 1
                    data["bans"]=bn_amount
                    new_ban = ({
                        "moderator": str(ctx.author.id),
                        "moderator_name": str(ctx.author.display_name),
                        "reason": rsn,
                        "datetime": dt_string,
                        "proof": ""
                    })
                    data[bn_amount]=new_ban
                    db.child("MODERATIONS").child("BANS").child(ctx.guild.id).child(member.id).set(data)

                    embed = disnake.Embed(
                        title = f"{member.name} has been banned.",
                        color = disnake.Color.dark_red()
                    )
                    embed.add_field(
                        name = f"Ban Info",
                        value = f"Moderator: {ctx.author.mention}\n"
                                f"Reason: **`{rsn}`**\n"
                                f"At: **``{dt_string}``**"
                    )
                await ctx.guild.ban(member, reason=f"By {ctx.author} was banned for {rsn}.")
                await ctx.send(embed=embed)
        except Forbidden:
            bot = ctx.guild.get_member(self.client.user.id)
            print(bot.guild_permissions.ban_members)
            if bot.guild_permissions.ban_members == False:
                await ctx.send("I don\'t have the required permissions to do that.\nPlease give me either `ban` permissions or `administrator`")
            else:
                await ctx.send("You can\'t ban that user.")

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(kick_members=True)
    @commands.check(moderation_check)
    async def kick(self, ctx, member:disnake.Member=None, *, reason=None):
        try:
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
                            "datetime": dt_string,
                            "proof": ""
                        })
                    })
                    db.child("MODERATIONS").child("KICKS").child(ctx.guild.id).child(member.id).set(data)
                    embed = disnake.Embed(
                        title = f"{member.name} has been kicked",
                        color = disnake.Color.dark_red()
                        )
                    embed.add_field(
                        name = "Kick info",
                        value = f"Moderator: {ctx.author.mention}\n"
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
                        "datetime": dt_string,
                        "proof": ""
                    })
                    data[kck_amount]=new_kick
                    db.child("MODERATIONS").child("KICKS").child(ctx.guild.id).child(member.id).set(data)

                    embed = disnake.Embed(
                        title = f"{member.name} has been kicked",
                        color = disnake.Color.dark_red()
                    )
                    embed.add_field(
                        name = f"Kick Info",
                        value = f"Moderator: {ctx.author.mention}\n"
                                f"Reason: **`{rsn}`**\n"
                                f"At: **``{dt_string}``**"
                    )
                    #await ctx.send(embed=embed)
                await ctx.guild.kick(member, reason=f"By {ctx.author} was kicked for {rsn}.")
                await ctx.send(embed=embed)
                #await ctx.send(f"{member} was kicked for {rsn}.")
        except Forbidden:
            if disnake.Permissions().kick_members == False:
                await ctx.send("I don\'t have the required permissions to do that.\nPlease give me either `kick` permissions or `administrator`")
                return
            else:
                await ctx.send("You can\'t kick that user.")
                return

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(ban_members=True)
    @commands.check(moderation_check)
    async def unban(self, ctx, id: int = None):
        #try:
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
        #except Forbidden:
        #    await ctx.send(f"I\'m missing permissions for this!\n{commands.MissingPermissions(missing_permissions=error.missing_permissions)}")
        #except Forbidden:
        #    await ctx.send(f"I\'m missing permissions for this!\n{disnake.ext.commands.MissingPermissions.missing_permissions()}")
        

def setup(client):
    client.add_cog(Moderation(client))
    print(f"Cog: Moderation - loaded.")

def teardown(client):
    print(f"Cog: Moderation - unloaded.")