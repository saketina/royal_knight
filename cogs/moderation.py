import datetime
import json
from datetime import datetime as dt

import disnake
import pyrebase
from disnake import Forbidden
from disnake.ext import commands

import logging

logging = logging.getLogger("Moderation")

# TODO ALL/add feature so its easy to add by role perms for commands

# TODO Add a notes tab for moderations similar to reason

firebase = pyrebase.initialize_app(json.load(open("./firebase_config.json", "r")))
db = firebase.database()

dt_string = dt.now().strftime("%d/%m/%Y %H:%M:%S")

staff_roles = 743724904033288293, 687228928565444800, 706540593865556071, 743724904033288293, 706161806426767470, 801614132771160095, 747680315257913384, 870431101955493999, 896472583212507206

ban_roles = 687228928565444800,706540593865556071, 743724904033288293, 706161806426767470, 801614132771160095, 747680315257913384
unban_roles = 687228928565444800, 706540593865556071, 743724904033288293, 706161806426767470, 801614132771160095
kick_roles = 687228928565444800, 706540593865556071, 743724904033288293, 706161806426767470, 801614132771160095, 747680315257913384, 870431101955493999
mute_roles = 687228928565444800, 706540593865556071, 743724904033288293, 706161806426767470, 801614132771160095, 747680315257913384, 870431101955493999, 896472583212507206
unmute_roles = 687228928565444800, 706540593865556071, 743724904033288293, 706161806426767470, 801614132771160095, 747680315257913384, 896472583212507206
warn_roles = 687228928565444800, 706540593865556071, 743724904033288293, 706161806426767470, 801614132771160095, 747680315257913384, 870431101955493999, 896472583212507206

def unmuted_check(member, mute_role):
    for role in member.roles:
        if role.id == mute_role:
            return False
        else:
            pass
    return True

def muted_check(member, mute_role):
    for role in member.roles:
        if role.id != mute_role:
            pass
        else:
            return True
    return False

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
        return False

def staff_check(member):
    try:
        return any((True for role in member.roles if role.id in staff_roles))
    except AttributeError:
        return False

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    # TODO add checks if roles exist in list(multiple-role-sys)
    # TODO when check is complete store roles unable to process to another list and output them to the user
    @commands.command()
    @commands.guild_only()
    async def role(self, ctx, action=None, command=None, *roles:disnake.Role):
        command_list = ["ban", "unban", "kick", "mute", "unmute", "warn", "purge"]
        
        help_embed = disnake.Embed(
                title = "insert help cmd",
                description = "work in progress...",
                color = disnake.Color.dark_red()
            )

        if action != "add" or action != "remove":
            await ctx.send(embed=help_embed)
            
        if command and roles == None:
            await ctx.send(embed=help_embed)
            
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
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member:disnake.Member=None, duration=None, *, reason=None):
        mute_role = db.child("SETUP").child(ctx.guild.id).child("MODERATION").child("MUTEROLE").get().val()
        if member == None:
            embed = disnake.Embed(
                title = "MUTE COMMAND",
                description = "``k.mute [member_id/@member] [duration] [reason]``",
                color = disnake.Color.dark_red()
                )
            embed.add_field(
                name="Duration Options",
                value="``` d = day/s\n"
                      " h = hour/s\n"
                      " m = minute/s\n"
                      " s = second/s```"
            )
            await ctx.send(embed=embed)
        if muted_check(member, mute_role) == True:
            await ctx.send("That user is already muted.")
            return
        if duration == None:
            duration = "28d"
        if reason == None:
            reason = "no reason"
        if member == ctx.author:
            await ctx.send("You can\'t mute yourself.")
            return
        if member.id == self.client.user.id:
            await ctx.send("Please don\'t mute me.")
            return
        elif staff_check(member) == True:
            await ctx.send("You can\'t mute that user.")
            return
        else:
            f = db.child("MODERATIONS").child("MUTES").child(ctx.guild.id).child(member.id).get().val()
            data = f
            if data == None:
                mute_amount = 1
                data = ({
                    "mutes": 1,
                    1:({
                        "moderator": str(ctx.author.id),
                        "moderator_name": str(ctx.author.display_name),
                        "reason": reason,
                        "datetime": dt_string
                    })
                })
                
                embed = disnake.Embed(
                    title = f"{member.name} has been muted for {duration}",
                    color = disnake.Color.dark_red()
                    )
                embed.add_field(
                    name = "Mute",
                    value = f"Mute ID: ``{mute_amount}``\nModerator: **``{ctx.author}``**\nReason: **`{reason}`**\nAt: **``{dt_string}``**",
                    inline = True
                    )
                if duration.endswith("s"):
                    seconds = int(duration[:-1])
                    minutes = 0.00
                    hours = 0.00
                    days = 0.00
                elif duration.endswith("m"):
                    seconds = 0.00
                    minutes = int(duration[:-1])
                    hours = 0.00
                    days = 0.00
                elif duration.endswith("h"):
                    seconds = 0.00
                    minutes = 0.00
                    hours = int(duration[:-1])
                    days = 0.00
                elif duration.endswith("d"):
                    seconds = 0.00
                    minutes = 0.00
                    hours = 0.00
                    days =int(duration[:-1]) 
                else:
                    seconds = 0.00
                    minutes = duration
                    hours = 0.00
                    days = 0.00

                time = datetime.timedelta(seconds=float(seconds), minutes=float(minutes), hours=float(hours), days=float(days))
                await member.timeout(duration=time, reason=reason)
                try:
                    await member.add_roles(mute_role)
                except:
                    guild = ctx.guild
                    mutedRole = disnake.utils.get(guild.roles, name="Muted")

                    if not mutedRole:
                        mutedRole = await guild.create_role(name="Muted")

                        for channel in guild.channels:
                            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
                    await member.add_roles(mutedRole)
                db.child("MODERATIONS").child("MUTES").child(ctx.guild.id).child(member.id).set(data)
                await ctx.send(embed=embed)
            else:
                mute_amount = data.get("mutes")
                mute_amount += 1
                data["mutes"]=mute_amount
                new_mute = ({
                    "moderator": str(ctx.author.id),
                    "moderator_name": str(ctx.author.display_name),
                    "reason": reason,
                    "datetime": dt_string
                })
                data[mute_amount]=new_mute
                #db.child("MODERATIONS").child("MUTES").child(ctx.guild.id).child(member.id).set(data)

                #await ctx.send(duration)
                if duration.endswith("s"):
                    seconds = int(duration[:-1])
                    minutes = 0.00
                    hours = 0.00
                    days = 0.00
                elif duration.endswith("m"):
                    seconds = 0.00
                    minutes = int(duration[:-1])
                    hours = 0.00
                    days = 0.00
                elif duration.endswith("h"):
                    seconds = 0.00
                    minutes = 0.00
                    hours = int(duration[:-1])
                    days = 0.00
                elif duration.endswith("d"):
                    seconds = 0.00
                    minutes = 0.00
                    hours = 0.00
                    days =int(duration[:-1]) 
                else:
                    seconds = 0.00
                    minutes = duration
                    hours = 0.00
                    days = 0.00

                embed = disnake.Embed(
                    title = f"{member.name} has been muted for {duration}",
                    color = disnake.Color.dark_red()
                )
                embed.add_field(
                    name = f"New Mute",
                    value = f"Mute ID: ``{mute_amount}``\nModerator: **``{ctx.author}``**\nReason: **`{reason}`**\nAt: **``{dt_string}``**"
                )

                time = datetime.timedelta(seconds=float(seconds), minutes=float(minutes), hours=float(hours), days=float(days))
                
                await member.timeout(duration=time, reason=reason)
                try:
                    await member.add_roles(mute_role)
                except:
                    guild = ctx.guild
                    mutedRole = disnake.utils.get(guild.roles, name="Muted")

                    if not mutedRole:
                        mutedRole = await guild.create_role(name="Muted")

                        for channel in guild.channels:
                            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
                    await member.add_roles(mutedRole)
                db.child("MODERATIONS").child("MUTES").child(ctx.guild.id).child(member.id).set(data)
                await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member:disnake.Member=None):
        mute_role = db.child("SETUP").child(ctx.guild.id).child("MODERATION").child("MUTEROLE").get().val()
        if member == None:
            embed = disnake.Embed(
                title = "UNMUTE COMMAND",
                description = "``k.unmute [member_id/@member]``",
                color = disnake.Color.dark_red()
                )
            await ctx.send(embed=embed)
        elif unmuted_check(member, mute_role) == True:
            await ctx.send("That user is not muted.")
        else:
            time = datetime.timedelta(seconds=0, minutes=0, days=0, hours=0)

            try:
                await member.remove_roles(mute_role)
            except:
                guild = ctx.guild
                mutedRole = disnake.utils.get(guild.roles, name="Muted")

                if not mutedRole:
                    mutedRole = await guild.create_role(name="Muted")

                    for channel in guild.channels:
                        await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
                await member.remove_roles(mutedRole)

            await member.timeout(duration=time)
            await ctx.send(f"{member.name} has been unmuted.")
    
    @commands.command()
    @commands.guild_only()
    @commands.check(moderation_check)
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
        elif staff_check(member) == True:
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
    async def ban(self, ctx, member:disnake.User=None, *, reason="For no reason"):
        if member in ctx.guild.members:
            member = member
        else:
            member = await ctx.guild.getch_member(member.id)
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
        elif staff_check(ctx.guild.get_member(member.id)) == True:
            await ctx.send("You can\'t ban that user.")
        else:
            f = db.child("MODERATIONS").child("BANS").child(ctx.guild.id).child(member.id).get().val()
            data = f
            if data == None:
                bn_amount = 1
                data = ({
                    "bans": 1,
                    1:({
                        "moderator": str(ctx.author.id),
                        "moderator_name": str(ctx.author.display_name),
                        "reason": reason,
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
                            f"Reason: **``{reason}``**\n"
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
                    "reason": reason,
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
                            f"Reason: **`{reason}`**\n"
                            f"At: **``{dt_string}``**"
                )
            await ctx.guild.ban(member, reason=f"By {ctx.author} was banned for {reason}.")
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(kick_members=True)
    @commands.check(moderation_check)
    async def kick(self, ctx, member:disnake.Member=None, *, reason="No reason"):
        if member==None:
            emb = disnake.Embed(
                title = "KICK HELP",
                description = "`k.kick [mention/user_id] (reason)`",
                color = disnake.Color.dark_red()
                )
            await ctx.send(embed=emb)
        elif member==ctx.author:
            await ctx.send(content = "You can\'t kick yourself", delete_after = 10)
        elif staff_check(member) == True:
            await ctx.send("You can\'t kick that user.")
        else:
            f = db.child("MODERATIONS").child("KICKS").child(ctx.guild.id).child(member.id).get().val()
            data = f
            if data == None:
                kck_amount = 1
                data = ({
                    "kicks": 1,
                    1:({
                        "moderator": str(ctx.author.id),
                        "moderator_name": str(ctx.author.display_name),
                        "reason": reason,
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
                            f"Reason: **``{reason}``**\n"
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
                    "reason": reason,
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
                            f"Reason: **`{reason}`**\n"
                            f"At: **``{dt_string}``**"
                )
                #await ctx.send(embed=embed)
            await ctx.guild.kick(member, reason=f"By {ctx.author} was kicked for {reason}.")
            await ctx.send(embed=embed)
            #await ctx.send(f"{member} was kicked for {reason}.")

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(ban_members=True)
    @commands.check(moderation_check)
    async def unban(self, ctx, target: disnake.User = None):
        if target == None:
            emb = disnake.Embed(
                title = "UNBAN HELP",
                description = "`k.unban [user_id]`",
                color = disnake.Color.dark_red()
                )
            await ctx.send(embed=emb)
        elif target == ctx.author:
            await ctx.send(content = "You aren\'t banned.", delete_after = 10)
        else:
            user = await self.client.fetch_user(target.id)
            await ctx.guild.unban(user)
            await ctx.send(f"{user} has been unbanned.")
        
def setup(client):
    client.add_cog(Moderation(client))