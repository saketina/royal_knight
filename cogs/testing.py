import datetime
import json
import os
from datetime import datetime as dt

import disnake
import pyrebase
from disnake.ext import commands
from disnake.ext.commands import Paginator, has_permissions
from disnake.ui import Button, View
from disnake.utils import get

# //TODO remove unneeded imports and lines of code
# //TODO transfer finished commands to appropriate cogs
# //TODO transfer buttons to emojies for moderations

firebase = pyrebase.initialize_app(json.load(open("firebase_config.json", "r")))
db = firebase.database()

dt_string = dt.now().strftime("%d/%m/%Y %H:%M:%S")

def author_check(ctx, interaction):
    if interaction.author.id == ctx.author.id:
        return True
    else:
        return False


class MyView(disnake.ui.View):
    def __init__(self, timeout: float, interaction:disnake.Interaction):
        super().__init__(timeout=timeout)

    async def on_timeout(self):
        try:
            if self.message != None:  # type: ignore
                await self.message.edit(view=None) # type: ignore
        except:
            interaction = self.interaction  # type: ignore
            await interaction.edit_original_message(view=None)

class Testing(commands.Cog):
    def __init__(self, client):
        self.client=client
        self.current_page = 0
        self.pages = {}
        self.pages_list = {}

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member:disnake.Member=None, duration=None, *, reason=None):
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
        elif duration == None:
            duration = "28d"
        elif reason == None:
            reason = "no reason"
        elif member == ctx.author:
            await ctx.send("You can\'t mute yourself.")
        elif member.id == self.client.user.id:
            await ctx.send("Please don\'t mute me.")
        elif member.guild_permissions.manage_messages == True:
            await ctx.send("You can\'t mute that user.")
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
                    seconds = duration.split(-1)
                    minutes = 0
                    hours = 0
                    days = 0
                elif duration.endswith("m"):
                    seconds = 0
                    minutes = duration.split(-1)
                    hours = 0
                    days = 0
                elif duration.endswith("h"):
                    seconds = 0
                    minutes = 0
                    hours = duration.split(-1)
                    days = 0
                elif duration.endswith("d"):
                    seconds = 0
                    minutes = 0
                    hours = 0
                    days = duration.split(-1)
                else:
                    minutes=duration

                time = datetime.timedelta(seconds=seconds, minutes=minutes, days=days, hours=hours)
                #until = utils.utcnow() + datetime.timedelta(seconds=duration)
                await member.timeout(time, reason=reason)
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
                    seconds = duration.replace("s", "")
                    minutes = 0
                    hours = 0
                    days = 0
                    suffix = "seconds"
                elif duration.endswith("m"):
                    seconds = 0
                    minutes = duration.replace("m", "")
                    hours = 0
                    days = 0
                    suffix = "minutes"
                elif duration.endswith("h"):
                    seconds = 0
                    minutes = 0
                    hours = duration.replace("h", "")
                    days = 0
                    suffix = "hours"
                elif duration.endswith("d"):
                    seconds = 0
                    minutes = 0
                    hours = 0
                    days = duration.replace("d", "")
                    suffix = "days"
                else:
                    seconds = 0
                    minutes = duration
                    hours = 0
                    days = 0
                    suffix = "minutes"

                embed = disnake.Embed(
                    title = f"{member.name} has been muted for {duration}",
                    color = disnake.Color.dark_red()
                )
                embed.add_field(
                    name = f"New Mute",
                    value = f"Mute ID: ``{mute_amount}``\nModerator: **``{ctx.author}``**\nReason: **`{reason}`**\nAt: **``{dt_string}``**"
                )

                time = datetime.timedelta(seconds=int(seconds), minutes=int(minutes), days=int(days), hours=int(hours))

                try:
                    await member.add_roles(1125541804654215350)
                except:
                    guild = ctx.guild
                    mutedRole = disnake.utils.get(guild.roles, name="Muted")

                    if not mutedRole:
                        mutedRole = await guild.create_role(name="Muted")

                        for channel in guild.channels:
                            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
                    await member.add_roles(mutedRole)

                await member.timeout(duration=time, reason=reason)
                #await member.add_roles(mutedRole, reason=reason)
                db.child("MODERATIONS").child("MUTES").child(ctx.guild.id).child(member.id).set(data)
                await ctx.send(embed=embed)

    @commands.command()
    async def unmute(self, ctx, member:disnake.Member=None):
        if member == None:
            embed = disnake.Embed(
                title = "UNMUTE COMMAND",
                description = "``k.unmute [member_id/@member]``",
                color = disnake.Color.dark_red()
                )
            await ctx.send(embed=embed)
        else:
            time = datetime.timedelta(seconds=0, minutes=0, days=0, hours=0)

            try:
                await member.remove_roles(1125541804654215350)
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

    @commands.command(aliases=["warns", "check", "moderations"], pass_context=True)
    async def warnings(self, ctx, user:disnake.User=None):
        try:
            self.pages_list.popitem(user.id)
        except:
            pass
        if user == None:
            embed = disnake.Embed(
                title = "WARNINGS COMMAND",
                description = "``k.mute [member_id/@member] [duration] [reason]``",
                color = disnake.Color.dark_red()
                )
            embed.add_field(
                name="Aliases",
                value="``` Warns\n"
                      " Check\n"
                      " Moderations\n"
                      " Warnings(default)```"
            )
            await ctx.send(embed=embed)
        else:
            db_warns = db.child("MODERATIONS").child("WARNS").child(ctx.guild.id).child(user.id).get().val()
            db_bans = db.child("MODERATIONS").child("BANS").child(ctx.guild.id).child(user.id).get().val()
            db_kicks = db.child("MODERATIONS").child("KICKS").child(ctx.guild.id).child(user.id).get().val()
            db_moderations = [db_warns, db_bans, db_kicks]

            db_warns.popitem("warns") if db_warns != None else None
            db_bans.popitem("bans") if db_bans != None else None
            db_kicks.popitem("kicks") if db_kicks != None else None
 
            if db_moderations != [None, None, None]:
                warnings_embed = disnake.Embed(
                    title = f"{user.name}\'s moderations",
                    description = "1. Warns\n2. Bans\n3. Kicks",
                    color = disnake.Color.dark_red()
                )

                button_warns = Button(label="Warns", disabled = True if db_warns == None else False)
                button_bans = Button(label="Bans", disabled = True if db_bans == None else False)
                button_kicks = Button(label="Kicks", disabled = True if db_kicks == None else False)

                async def button_warns_callback(interaction):
                    button_warns_delete = Button(label="Delete", style = disnake.ButtonStyle.red)
                    button_warns_edit = Button(label="Edit")
                    button_warns_exit = Button(label="Exit")
                    button_warns_next = Button(label="Next", disabled = False)
                    button_warns_previous = Button(label="Previous", disabled=True)

                    if author_check(ctx, interaction):
                            moderation = db.child("MODERATIONS").child("WARNS").child(ctx.guild.id).child(user.id).get().val()
                            if db_warns != None:
                                moderation.popitem(str("warns"))

                                #self.warn_number[user.id] = 0
                                warn_number = 0
                                #self.page_number[user.id] = 0
                                page_number = 0
                                self.pages = {}
                                for key in moderation:

                                    warn = db.child("MODERATIONS").child("WARNS").child(ctx.guild.id).child(user.id).child(key).get().val()

                                    warn_number += 1
                                    warn_id = key
                                    warn_count = len(moderation)
                                    time = warn["datetime"]
                                    mod_id = warn["moderator"]
                                    mod_name = warn["moderator_name"]
                                    reason = warn["reason"]
                                    
                                    embed = disnake.Embed(
                                        title=f"{user.name}\'s Warnings",
                                        color=disnake.Color.dark_red()
                                    )
                                    embed.add_field(
                                    name = f"{warn_number}/{warn_count}",
                                    value = f"Warn ID: ``{warn_id}``\n\n"
                                            f"Mod ID: ``{mod_id}``\n"
                                            f"Mod: <@!{mod_id}>\n\n"
                                            f"Member ID: {user.id}\n"
                                            f"Member: <@!{user.id}>\n"
                                            f"Reason: ``{reason}``\n"
                                            f"At: ``{time}``"
                                    )

                                    page_number += 1
                                    self.pages[page_number] = embed

                                self.pages_list[user.id] = self.pages
                                pages = self.pages_list[user.id]
                                self.current_page = 1

                                async def button_warns_edit_callback(interaction):
                                    if interaction.author.id == ctx.author.id:
                                        await interaction.response.defer(with_message = False)

                                        def check(m):
                                            return m.author == ctx.author and m.channel == ctx.channel

                                        await ctx.send("What do you want me to change the reason to?")

                                        msg = await self.client.wait_for('message', check=check)

                                        edit_embed = disnake.Embed(
                                            title = f"{user.name}\'s Warnings",
                                            color = disnake.Color.dark_red()
                                            )

                                        mod_id = warn["moderator"]
                                        time = warn["datetime"]

                                        edit_embed.add_field(
                                            name = f"{warn_number}/{warn_count}",
                                            value = f"Warn ID: ``{warn_id}``\n\n"
                                                    f"Mod ID: ``{mod_id}``\n"
                                                    f"Mod: <@!{mod_id}>\n\n"
                                                    f"Member ID: {user.id}\n"
                                                    f"Member: <@!{user.id}>\n"
                                                    f"Reason: ``{msg.content}``\n"
                                                    f"At: ``{time}``"
                                                    )
                                        #edit_embed.set_footer(text = {dt.now()})

                                        db.child("MODERATIONS").child("WARNS").child(ctx.guild.id).child(user.id).child(self.current_page).update({"reason": str(msg.content)})
                                        await ctx.send("The moderation has been changed.")
                                        await interaction.edit_original_response(embed = edit_embed, view = None)

                                async def button_warns_delete_callback(interaction):
                                    if interaction.author.id == ctx.author.id:
                                        button_warns_yes = Button(label="Yes", style=disnake.ButtonStyle.green)
                                        button_warns_no = Button(label="No", style=disnake.ButtonStyle.red)

                                    async def button_warns_yes_callback(interaction):
                                        if interaction.author.id == ctx.author.id:
                                            await interaction.response.defer(with_message = False)
                                            db.child("MODERATIONS").child("WARNS").child(ctx.guild.id).child(user.id).child(self.current_page).remove()
                                            await interaction.edit_original_response(content="The warn has been deleted 🚮", view=None)
                                        else:
                                            return

                                    async def button_warns_no_callback(interaction):
                                        if interaction.author.id == ctx.author.id:
                                            await interaction.response.edit_message(content="I didn\'t delete any warn", view=None)
                                        else:
                                            return

                                    button_warns_yes.callback = button_warns_yes_callback
                                    button_warns_no.callback = button_warns_no_callback

                                    view = MyView(timeout=30, interaction=[button_warns_yes_callback, button_warns_no_callback])
                                    view.add_item(button_warns_yes)
                                    view.add_item(button_warns_no)

                                    MyView.message = await ctx.send("Are you sure?", view=view)
                                    await interaction.response.edit_message(view=None)

                                async def button_warns_exit_callback(interaction):
                                    if interaction.author.id == ctx.author.id:
                                        await interaction.response.edit_message(view=None)
                                
                                async def button_warns_previous_previous_callback(interaction):
                                    # print("started-previous_previous")
                                    if interaction.author.id == ctx.author.id:                                      
                                        self.current_page -= 1
                                        if self.current_page == 1:
                                            button_warns_previous = Button(label="Previous", disabled=True)
                                        else:
                                            button_warns_previous = Button(label="Previous", disabled=False)

                                        button_warns_previous.callback=button_warns_previous_callback
                                        
                                        view = MyView(timeout=30, interaction=[button_warns_delete_callback, button_warns_edit_callback, button_warns_exit_callback, button_warns_next_callback, button_warns_previous_callback])
                                        view.add_item(button_warns_previous)
                                        view.add_item(button_warns_delete)
                                        view.add_item(button_warns_edit)
                                        view.add_item(button_warns_exit)
                                        view.add_item(button_warns_next)
                                        MyView.message = await interaction.response.edit_message(embed=pages[self.current_page], view=view)
                            
                                async def button_warns_previous_callback(interaction):
                                    # print("started-previous")
                                    if interaction.author.id == ctx.author.id:
                                        self.current_page -= 1
                                        if self.current_page == 1:
                                            button_warns_previous = Button(label="Previous", disabled=True)
                                        else:
                                            button_warns_previous = Button(label="Previous", disabled=False)

                                        button_warns_previous.callback=button_warns_previous_previous_callback
                                        
                                        view = MyView(timeout=30, interaction=[button_warns_delete_callback, button_warns_edit_callback, button_warns_exit_callback, button_warns_next_next_callback, button_warns_previous_previous_callback])
                                        view.add_item(button_warns_previous)
                                        view.add_item(button_warns_delete)
                                        view.add_item(button_warns_edit)
                                        view.add_item(button_warns_exit)
                                        view.add_item(button_warns_next)
                                        MyView.message = await interaction.response.edit_message(embed=pages[self.current_page], view=view)
                            
                                async def button_warns_next_next_callback(interaction):
                                    # print("started-next_next")
                                    if interaction.author.id == ctx.author.id:
                                        self.current_page += 1

                                        if self.current_page == page_number:
                                            button_warns_next = Button(label="Next", disabled=True)
                                        elif self.current_page >= page_number:
                                            button_warns_next = Button(label="Next", disabled=True)
                                        else:
                                            button_warns_next = Button(label="Next", disabled=False)

                                        if self.current_page == 1:
                                            button_warns_previous = Button(label="Previous", disabled=True)
                                        else:
                                            button_warns_previous = Button(label="Previous", disabled=False)

                                        button_warns_next.callback=button_warns_next_callback
                                        button_warns_previous.callback=button_warns_previous_previous_callback
                                        
                                        view = MyView(timeout=30, interaction=[button_warns_delete_callback, button_warns_edit_callback, button_warns_exit_callback, button_warns_next_callback, button_warns_previous_previous_callback])
                                        view.add_item(button_warns_previous)
                                        view.add_item(button_warns_delete)
                                        view.add_item(button_warns_edit)
                                        view.add_item(button_warns_exit)
                                        view.add_item(button_warns_next)
                                        MyView.message = await interaction.response.edit_message(embed=pages[self.current_page], view=view)
                                
                                async def button_warns_next_callback(interaction):
                                    # print("started-next")
                                    if interaction.author.id == ctx.author.id:
                                        self.current_page += 1

                                        if self.current_page == page_number:
                                            button_warns_next = Button(label="Next", disabled=True)
                                        elif self.current_page >= page_number:
                                            button_warns_next = Button(label="Next", disabled=True)
                                        else:
                                            button_warns_next = Button(label="Next", disabled=False)
                                        
                                        if self.current_page == 1:
                                            button_warns_previous = Button(label="Previous", disabled=True)
                                        else:
                                            button_warns_previous = Button(label="Previous", disabled=False)

                                        button_warns_next.callback=button_warns_next_next_callback
                                        button_warns_previous.callback=button_warns_previous_previous_callback
                                        
                                        view = MyView(timeout=30, interaction=[button_warns_delete_callback, button_warns_edit_callback, button_warns_exit_callback, button_warns_next_next_callback, button_warns_previous_previous_callback])
                                        view.add_item(button_warns_previous)
                                        view.add_item(button_warns_delete)
                                        view.add_item(button_warns_edit)
                                        view.add_item(button_warns_exit)
                                        view.add_item(button_warns_next)
                                        MyView.message = await interaction.response.edit_message(embed=pages[self.current_page], view=view)

                                if self.current_page == page_number:
                                            button_warns_next = Button(label="Next", disabled=True)
                                elif self.current_page >= page_number:
                                    button_warns_next = Button(label="Next", disabled=True)
                                else:
                                    button_warns_next = Button(label="Next", disabled=False)

                                button_warns_delete.callback = button_warns_delete_callback
                                button_warns_edit.callback = button_warns_edit_callback
                                button_warns_exit.callback = button_warns_exit_callback
                                button_warns_next.callback = button_warns_next_callback
                                button_warns_previous.callback = button_warns_previous_callback

                                view_warns = MyView(timeout=30, interaction=[button_warns_delete_callback, button_warns_edit_callback, button_warns_exit_callback, button_warns_previous_callback])
                                view_warns.add_item(button_warns_previous)
                                view_warns.add_item(button_warns_delete)
                                view_warns.add_item(button_warns_edit)
                                view_warns.add_item(button_warns_exit)
                                view_warns.add_item(button_warns_next)
                                MyView.message = await interaction.response.edit_message(embed=pages[self.current_page], view=view_warns)
                            else:
                                print("There aren't any moderations")

                    else:
                        return

                async def button_bans_callback(interaction):
                    button_bans_delete = Button(label="Delete", style = disnake.ButtonStyle.red)
                    button_bans_edit = Button(label="Edit")
                    button_bans_exit = Button(label="Exit")
                    button_bans_next = Button(label="Next", disabled = False)
                    button_bans_previous = Button(label="Previous", disabled=True)

                    if author_check(ctx, interaction):
                            moderation = db.child("MODERATIONS").child("BANS").child(ctx.guild.id).child(user.id).get().val()
                            if db_bans != None:
                                moderation.popitem(str("bans"))

                                #self.ban_number[user.id] = 0
                                ban_number = 0
                                #self.page_number[user.id] = 0
                                page_number = 0
                                self.pages = {}
                                for key in moderation:

                                    ban = db.child("MODERATIONS").child("BANS").child(ctx.guild.id).child(user.id).child(key).get().val()

                                    ban_number += 1
                                    ban_id = key
                                    ban_count = len(moderation)
                                    time = ban["datetime"]
                                    mod_id = ban["moderator"]
                                    mod_name = ban["moderator_name"]
                                    reason = ban["reason"]
                                    
                                    embed = disnake.Embed(
                                        title=f"{user.name}\'s Bans",
                                        color=disnake.Color.dark_red()
                                    )
                                    embed.add_field(
                                    name = f"{ban_number}/{ban_count}",
                                    value = f"Ban ID: ``{ban_id}``\n\n"
                                            f"Mod ID: ``{mod_id}``\n"
                                            f"Mod: <@!{mod_id}>\n\n"
                                            f"Member ID: {user.id}\n"
                                            f"Member: <@!{user.id}>\n"
                                            f"Reason: ``{reason}``\n"
                                            f"At: ``{time}``"
                                    )

                                    page_number += 1
                                    self.pages[page_number] = embed

                                self.pages_list[user.id] = self.pages
                                pages = self.pages_list[user.id]
                                self.current_page = 1

                                async def button_bans_edit_callback(interaction):
                                    if interaction.author.id == ctx.author.id:
                                        await interaction.response.defer(with_message = False)

                                        def check(m):
                                            return m.author == ctx.author and m.channel == ctx.channel

                                        await ctx.send("What do you want me to change the reason to?")

                                        msg = await self.client.wait_for('message', check=check)

                                        edit_embed = disnake.Embed(
                                            title = f"{user.name}\'s Bans",
                                            color = disnake.Color.dark_red()
                                            )

                                        mod_id = ban["moderator"]
                                        time = ban["datetime"]

                                        edit_embed.add_field(
                                            name = f"{ban_number}/{ban_count}",
                                            value = f"Ban ID: ``{ban_id}``\n\n"
                                                    f"Mod ID: ``{mod_id}``\n"
                                                    f"Mod: <@!{mod_id}>\n\n"
                                                    f"Member ID: {user.id}\n"
                                                    f"Member: <@!{user.id}>\n"
                                                    f"Reason: ``{msg.content}``\n"
                                                    f"At: ``{time}``"
                                                    )
                                        #edit_embed.set_footer(text = {dt.now()})

                                        db.child("MODERATIONS").child("BANS").child(ctx.guild.id).child(user.id).child(self.current_page).update({"reason": str(msg.content)})
                                        await ctx.send("The moderation has been changed.")
                                        await interaction.edit_original_response(embed = edit_embed, view = None)

                                async def button_bans_delete_callback(interaction):
                                    if interaction.author.id == ctx.author.id:
                                        button_bans_yes = Button(label="Yes", style=disnake.ButtonStyle.green)
                                        button_bans_no = Button(label="No", style=disnake.ButtonStyle.red)

                                    async def button_bans_yes_callback(interaction):
                                        if interaction.author.id == ctx.author.id:
                                            await interaction.response.defer(with_message = False)
                                            db.child("MODERATIONS").child("BANS").child(ctx.guild.id).child(user.id).child(self.current_page).remove()
                                            await interaction.edit_original_response(content="The moderation has been deleted 🚮", view=None)
                                        else:
                                            return

                                    async def button_bans_no_callback(interaction):
                                        if interaction.author.id == ctx.author.id:
                                            await interaction.response.edit_message(content="I didn\'t delete any moderation", view=None)
                                        else:
                                            return

                                    button_bans_yes.callback = button_bans_yes_callback
                                    button_bans_no.callback = button_bans_no_callback

                                    view = MyView(timeout=30, interaction=[button_bans_yes_callback, button_bans_no_callback])
                                    view.add_item(button_bans_yes)
                                    view.add_item(button_bans_no)

                                    MyView.message = await ctx.send("Are you sure?", view=view)
                                    await interaction.response.edit_message(view=None)

                                async def button_bans_exit_callback(interaction):
                                    if interaction.author.id == ctx.author.id:
                                        await interaction.response.edit_message(view=None)
                                
                                async def button_bans_previous_previous_callback(interaction):
                                    # print("started-previous_previous")
                                    if interaction.author.id == ctx.author.id:                                      
                                        self.current_page -= 1
                                        if self.current_page == 1:
                                            button_bans_previous = Button(label="Previous", disabled=True)
                                        else:
                                            button_bans_previous = Button(label="Previous", disabled=False)

                                        button_bans_previous.callback=button_bans_previous_callback
                                        
                                        view = MyView(timeout=30, interaction=[button_bans_delete_callback, button_bans_edit_callback, button_bans_exit_callback, button_bans_next_callback, button_bans_previous_callback])
                                        view.add_item(button_bans_previous)
                                        view.add_item(button_bans_delete)
                                        view.add_item(button_bans_edit)
                                        view.add_item(button_bans_exit)
                                        view.add_item(button_bans_next)
                                        MyView.message = await interaction.response.edit_message(embed=pages[self.current_page], view=view)
                            
                                async def button_bans_previous_callback(interaction):
                                    # print("started-previous")
                                    if interaction.author.id == ctx.author.id:
                                        self.current_page -= 1
                                        if self.current_page == 1:
                                            button_bans_previous = Button(label="Previous", disabled=True)
                                        else:
                                            button_bans_previous = Button(label="Previous", disabled=False)

                                        button_bans_previous.callback=button_bans_previous_previous_callback
                                        
                                        view = MyView(timeout=30, interaction=[button_bans_delete_callback, button_bans_edit_callback, button_bans_exit_callback, button_bans_next_next_callback, button_bans_previous_previous_callback])
                                        view.add_item(button_bans_previous)
                                        view.add_item(button_bans_delete)
                                        view.add_item(button_bans_edit)
                                        view.add_item(button_bans_exit)
                                        view.add_item(button_bans_next)
                                        MyView.message = await interaction.response.edit_message(embed=pages[self.current_page], view=view)
                            
                                async def button_bans_next_next_callback(interaction):
                                    # print("started-next_next")
                                    if interaction.author.id == ctx.author.id:
                                        self.current_page += 1

                                        if self.current_page == page_number:
                                            button_bans_next = Button(label="Next", disabled=True)
                                        elif self.current_page >= page_number:
                                            button_bans_next = Button(label="Next", disabled=True)
                                        else:
                                            button_bans_next = Button(label="Next", disabled=False)

                                        if self.current_page == 1:
                                            button_bans_previous = Button(label="Previous", disabled=True)
                                        else:
                                            button_bans_previous = Button(label="Previous", disabled=False)

                                        button_bans_next.callback=button_bans_next_callback
                                        button_bans_previous.callback=button_bans_previous_previous_callback
                                        
                                        view = MyView(timeout=30, interaction=[button_bans_delete_callback, button_bans_edit_callback, button_bans_exit_callback, button_bans_next_callback, button_bans_previous_previous_callback])
                                        view.add_item(button_bans_previous)
                                        view.add_item(button_bans_delete)
                                        view.add_item(button_bans_edit)
                                        view.add_item(button_bans_exit)
                                        view.add_item(button_bans_next)
                                        MyView.message = await interaction.response.edit_message(embed=pages[self.current_page], view=view)
                                
                                async def button_bans_next_callback(interaction):
                                    # print("started-next")
                                    if interaction.author.id == ctx.author.id:
                                        self.current_page += 1

                                        if self.current_page == page_number:
                                            button_bans_next = Button(label="Next", disabled=True)
                                        elif self.current_page >= page_number:
                                            button_bans_next = Button(label="Next", disabled=True)
                                        else:
                                            button_bans_next = Button(label="Next", disabled=False)
                                        
                                        if self.current_page == 1:
                                            button_bans_previous = Button(label="Previous", disabled=True)
                                        else:
                                            button_bans_previous = Button(label="Previous", disabled=False)

                                        button_bans_next.callback=button_bans_next_next_callback
                                        button_bans_previous.callback=button_bans_previous_previous_callback
                                        
                                        view = MyView(timeout=30, interaction=[button_bans_delete_callback, button_bans_edit_callback, button_bans_exit_callback, button_bans_next_next_callback, button_bans_previous_previous_callback])
                                        view.add_item(button_bans_previous)
                                        view.add_item(button_bans_delete)
                                        view.add_item(button_bans_edit)
                                        view.add_item(button_bans_exit)
                                        view.add_item(button_bans_next)
                                        MyView.message = await interaction.response.edit_message(embed=pages[self.current_page], view=view)

                                if self.current_page == page_number:
                                            button_bans_next = Button(label="Next", disabled=True)
                                elif self.current_page >= page_number:
                                    button_bans_next = Button(label="Next", disabled=True)
                                else:
                                    button_bans_next = Button(label="Next", disabled=False)

                                button_bans_delete.callback = button_bans_delete_callback
                                button_bans_edit.callback = button_bans_edit_callback
                                button_bans_exit.callback = button_bans_exit_callback
                                button_bans_next.callback = button_bans_next_callback
                                button_bans_previous.callback = button_bans_previous_callback

                                view_bans = MyView(timeout=30, interaction=[button_bans_delete_callback, button_bans_edit_callback, button_bans_exit_callback, button_bans_previous_callback])
                                view_bans.add_item(button_bans_previous)
                                view_bans.add_item(button_bans_delete)
                                view_bans.add_item(button_bans_edit)
                                view_bans.add_item(button_bans_exit)
                                view_bans.add_item(button_bans_next)
                                MyView.message = await interaction.response.edit_message(embed=pages[self.current_page], view=view_bans)
                            else:
                                print("There aren't any moderations")

                    else:
                        return

                async def button_kicks_callback(interaction):
                    button_kicks_delete = Button(label="Delete", style = disnake.ButtonStyle.red)
                    button_kicks_edit = Button(label="Edit")
                    button_kicks_exit = Button(label="Exit")
                    button_kicks_next = Button(label="Next", disabled = False)
                    button_kicks_previous = Button(label="Previous", disabled=True)

                    if author_check(ctx, interaction):
                            moderation = db.child("MODERATIONS").child("KICKS").child(ctx.guild.id).child(user.id).get().val()
                            if db_kicks != None:
                                moderation.popitem(str("kicks"))

                                #self.kick_number[user.id] = 0
                                kick_number = 0
                                #self.page_number[user.id] = 0
                                page_number = 0
                                self.pages = {}
                                for key in moderation:

                                    kick = db.child("MODERATIONS").child("KICKS").child(ctx.guild.id).child(user.id).child(key).get().val()

                                    kick_number += 1
                                    kick_id = key
                                    kick_count = len(moderation)
                                    time = kick["datetime"]
                                    mod_id = kick["moderator"]
                                    mod_name = kick["moderator_name"]
                                    reason = kick["reason"]
                                    
                                    embed = disnake.Embed(
                                        title=f"{user.name}\'s Kicks",
                                        color=disnake.Color.dark_red()
                                    )
                                    embed.add_field(
                                    name = f"{kick_number}/{kick_count}",
                                    value = f"Kick ID: ``{kick_id}``\n\n"
                                            f"Mod ID: ``{mod_id}``\n"
                                            f"Mod: <@!{mod_id}>\n\n"
                                            f"Member ID: {user.id}\n"
                                            f"Member: <@!{user.id}>\n"
                                            f"Reason: ``{reason}``\n"
                                            f"At: ``{time}``"
                                    )

                                    page_number += 1
                                    self.pages[page_number] = embed

                                self.pages_list[user.id] = self.pages
                                pages = self.pages_list[user.id]
                                self.current_page = 1

                                async def button_kicks_edit_callback(interaction):
                                    if interaction.author.id == ctx.author.id:
                                        await interaction.response.defer(with_message = False)

                                        def check(m):
                                            return m.author == ctx.author and m.channel == ctx.channel

                                        await ctx.send("What do you want me to change the reason to?")

                                        msg = await self.client.wait_for('message', check=check)

                                        edit_embed = disnake.Embed(
                                            title = f"{user.name}\'s Kicks",
                                            color = disnake.Color.dark_red()
                                            )

                                        mod_id = kick["moderator"]
                                        time = kick["datetime"]

                                        edit_embed.add_field(
                                            name = f"{kick_number}/{kick_count}",
                                            value = f"Kick ID: ``{kick_id}``\n\n"
                                                    f"Mod ID: ``{mod_id}``\n"
                                                    f"Mod: <@!{mod_id}>\n\n"
                                                    f"Member ID: {user.id}\n"
                                                    f"Member: <@!{user.id}>\n"
                                                    f"Reason: ``{msg.content}``\n"
                                                    f"At: ``{time}``"
                                                    )
                                        #edit_embed.set_footer(text = {dt.now()})

                                        db.child("MODERATIONS").child("KICKS").child(ctx.guild.id).child(user.id).child(self.current_page).update({"reason": str(msg.content)})
                                        await ctx.send("The moderation has been changed.")
                                        await interaction.edit_original_response(embed = edit_embed, view = None)

                                async def button_kicks_delete_callback(interaction):
                                    if interaction.author.id == ctx.author.id:
                                        button_kicks_yes = Button(label="Yes", style=disnake.ButtonStyle.green)
                                        button_kicks_no = Button(label="No", style=disnake.ButtonStyle.red)

                                    async def button_kicks_yes_callback(interaction):
                                        if interaction.author.id == ctx.author.id:
                                            await interaction.response.defer(with_message = False)
                                            db.child("MODERATIONS").child("KICKS").child(ctx.guild.id).child(user.id).child(self.current_page).remove()
                                            await interaction.edit_original_response(content="The moderation has been deleted 🚮", view=None)
                                        else:
                                            return

                                    async def button_kicks_no_callback(interaction):
                                        if interaction.author.id == ctx.author.id:
                                            await interaction.response.edit_message(content="I didn\'t delete any moderation", view=None)
                                        else:
                                            return

                                    button_kicks_yes.callback = button_kicks_yes_callback
                                    button_kicks_no.callback = button_kicks_no_callback

                                    view = MyView(timeout=30, interaction=[button_kicks_yes_callback, button_kicks_no_callback])
                                    view.add_item(button_kicks_yes)
                                    view.add_item(button_kicks_no)

                                    MyView.message = await ctx.send("Are you sure?", view=view)
                                    await interaction.response.edit_message(view=None)

                                async def button_kicks_exit_callback(interaction):
                                    if interaction.author.id == ctx.author.id:
                                        await interaction.response.edit_message(view=None)
                                
                                async def button_kicks_previous_previous_callback(interaction):
                                    # print("started-previous_previous")
                                    if interaction.author.id == ctx.author.id:                                      
                                        self.current_page -= 1
                                        if self.current_page == 1:
                                            button_kicks_previous = Button(label="Previous", disabled=True)
                                        else:
                                            button_kicks_previous = Button(label="Previous", disabled=False)

                                        button_kicks_previous.callback=button_kicks_previous_callback
                                        
                                        view = MyView(timeout=30, interaction=[button_kicks_delete_callback, button_kicks_edit_callback, button_kicks_exit_callback, button_kicks_next_callback, button_kicks_previous_callback])
                                        view.add_item(button_kicks_previous)
                                        view.add_item(button_kicks_delete)
                                        view.add_item(button_kicks_edit)
                                        view.add_item(button_kicks_exit)
                                        view.add_item(button_kicks_next)
                                        MyView.message = await interaction.response.edit_message(embed=pages[self.current_page], view=view)
                            
                                async def button_kicks_previous_callback(interaction):
                                    # print("started-previous")
                                    if interaction.author.id == ctx.author.id:
                                        self.current_page -= 1
                                        if self.current_page == 1:
                                            button_kicks_previous = Button(label="Previous", disabled=True)
                                        else:
                                            button_kicks_previous = Button(label="Previous", disabled=False)

                                        button_kicks_previous.callback=button_kicks_previous_previous_callback
                                        
                                        view = MyView(timeout=30, interaction=[button_kicks_delete_callback, button_kicks_edit_callback, button_kicks_exit_callback, button_kicks_next_next_callback, button_kicks_previous_previous_callback])
                                        view.add_item(button_kicks_previous)
                                        view.add_item(button_kicks_delete)
                                        view.add_item(button_kicks_edit)
                                        view.add_item(button_kicks_exit)
                                        view.add_item(button_kicks_next)
                                        MyView.message = await interaction.response.edit_message(embed=pages[self.current_page], view=view)
                            
                                async def button_kicks_next_next_callback(interaction):
                                    # print("started-next_next")
                                    if interaction.author.id == ctx.author.id:
                                        self.current_page += 1

                                        if self.current_page == page_number:
                                            button_kicks_next = Button(label="Next", disabled=True)
                                        elif self.current_page >= page_number:
                                            button_kicks_next = Button(label="Next", disabled=True)
                                        else:
                                            button_kicks_next = Button(label="Next", disabled=False)

                                        if self.current_page == 1:
                                            button_kicks_previous = Button(label="Previous", disabled=True)
                                        else:
                                            button_kicks_previous = Button(label="Previous", disabled=False)

                                        button_kicks_next.callback=button_kicks_next_callback
                                        button_kicks_previous.callback=button_kicks_previous_previous_callback
                                        
                                        view = MyView(timeout=30, interaction=[button_kicks_delete_callback, button_kicks_edit_callback, button_kicks_exit_callback, button_kicks_next_callback, button_kicks_previous_previous_callback])
                                        view.add_item(button_kicks_previous)
                                        view.add_item(button_kicks_delete)
                                        view.add_item(button_kicks_edit)
                                        view.add_item(button_kicks_exit)
                                        view.add_item(button_kicks_next)
                                        MyView.message = await interaction.response.edit_message(embed=pages[self.current_page], view=view)
                                
                                async def button_kicks_next_callback(interaction):
                                    # print("started-next")
                                    if interaction.author.id == ctx.author.id:
                                        self.current_page += 1

                                        if self.current_page == page_number:
                                            button_kicks_next = Button(label="Next", disabled=True)
                                        elif self.current_page >= page_number:
                                            button_kicks_next = Button(label="Next", disabled=True)
                                        else:
                                            button_kicks_next = Button(label="Next", disabled=False)
                                        
                                        if self.current_page == 1:
                                            button_kicks_previous = Button(label="Previous", disabled=True)
                                        else:
                                            button_kicks_previous = Button(label="Previous", disabled=False)

                                        button_kicks_next.callback=button_kicks_next_next_callback
                                        button_kicks_previous.callback=button_kicks_previous_previous_callback
                                        
                                        view = MyView(timeout=30, interaction=[button_kicks_delete_callback, button_kicks_edit_callback, button_kicks_exit_callback, button_kicks_next_next_callback, button_kicks_previous_previous_callback])
                                        view.add_item(button_kicks_previous)
                                        view.add_item(button_kicks_delete)
                                        view.add_item(button_kicks_edit)
                                        view.add_item(button_kicks_exit)
                                        view.add_item(button_kicks_next)
                                        MyView.message = await interaction.response.edit_message(embed=pages[self.current_page], view=view)

                                if self.current_page == page_number:
                                            button_kicks_next = Button(label="Next", disabled=True)
                                elif self.current_page >= page_number:
                                    button_kicks_next = Button(label="Next", disabled=True)
                                else:
                                    button_kicks_next = Button(label="Next", disabled=False)

                                button_kicks_delete.callback = button_kicks_delete_callback
                                button_kicks_edit.callback = button_kicks_edit_callback
                                button_kicks_exit.callback = button_kicks_exit_callback
                                button_kicks_next.callback = button_kicks_next_callback
                                button_kicks_previous.callback = button_kicks_previous_callback

                                view_kicks = MyView(timeout=30, interaction=[button_kicks_delete_callback, button_kicks_edit_callback, button_kicks_exit_callback, button_kicks_previous_callback])
                                view_kicks.add_item(button_kicks_previous)
                                view_kicks.add_item(button_kicks_delete)
                                view_kicks.add_item(button_kicks_edit)
                                view_kicks.add_item(button_kicks_exit)
                                view_kicks.add_item(button_kicks_next)
                                MyView.message = await interaction.response.edit_message(embed=pages[self.current_page], view=view_kicks)
                            else:
                                print("There aren't any moderations")

                    else:
                        return
                
                async def on_error(self, error, item, interaction):
                    print(error)

                button_warns.callback = button_warns_callback
                button_bans.callback = button_bans_callback
                button_kicks.callback = button_kicks_callback

                view_select = MyView(timeout=30, interaction=[button_warns_callback])

                view_select.add_item(button_warns)
                view_select.add_item(button_bans)
                view_select.add_item(button_kicks)

                MyView.message = await ctx.send(embed=warnings_embed, view=view_select)
            else:
                await ctx.send("I see no moderations")

    @commands.command()
    async def test_button(self, ctx):
        button = Button(label="button-kun")

        async def button_callback(interaction):
            print("Button-kun added!")

        button.callback = button_callback

        view = MyView(timeout=10)
        view.add_item(button)
        await ctx.send(content="Testing...", view=view)

    @commands.command()
    async def test_warn(self, ctx, user:disnake.User=None, inter: disnake.ApplicationCommandInteraction=None):
        moderation = db.child("MODERATIONS").child("WARNS").child(ctx.guild.id).child(user.id).get().val()
        #await ctx.send(moderation)
        #moderation_count = len(moderation)
        #await ctx.send(moderation_count)
        
        moderation.popitem(str("warns"))
        #await ctx.send(moderation)
        self.warn_number[user.id] = 0
        self.page_number[user.id] = 0
        self.pages = {}
        for key in moderation:
            #print(key)
            warn = db.child("MODERATIONS").child("WARNS").child(ctx.guild.id).child(user.id).child(key).get().val()

            self.warn_number += 1
            warn_id = key
            warn_count = len(moderation)
            time = warn["datetime"]
            mod_id = warn["moderator"]
            mod_name = warn["moderator_name"]
            reason = warn["reason"]
            
            embed = disnake.Embed(
                title=f"{user.name}\'s Warnings",
                color=disnake.Color.dark_red()
            )
            embed.add_field(
            name = f"{self.warn_number}/{warn_count}",
            value = f"Warn ID: ``{warn_id}``\n\n"
                    f"Mod ID: ``{mod_id}``\n"
                    f"Mod: <@!{mod_id}>\n\n"
                    f"Member ID: {user.id}\n"
                    f"Member: <@!{user.id}>\n"
                    f"Reason: ``{reason}``\n"
                    f"At: ``{time}``"
            )

            self.page_number += 1
            self.pages[self.page_number] = embed

        self.pages_list[user.id] = self.pages
        pages = self.pages_list[user.id]

        await ctx.send(embed=pages[1])
        await ctx.send(embed=pages[2])

    @commands.command(aliases=["wrns"], pass_context=True)
    async def testing(self, ctx, user:disnake.User=None, inter: disnake.ApplicationCommandInteraction = None):
        if user == None:
            await ctx.send("Please tell me who to check.")
        else:
            db_warns = db.child("MODERATIONS").child("WARNS").child(ctx.guild.id).child(user.id).get()
            db_bans = db.child("MODERATIONS").child("BANS").child(ctx.guild.id).child(user.id).get()
            db_kicks = db.child("MODERATIONS").child("KICKS").child(ctx.guild.id).child(user.id).get()
            db_moderations = [db_warns, db_bans, db_kicks]

            if db_moderations != [None, None, None]:
                warnings_embed = disnake.Embed(
                    title = f"{user.name}\'s moderations",
                    description = "1. Warns\n2. Bans\n3. Kicks",
                    color = disnake.Color.dark_red()
                )

                button_warns = Button(label="Warns", disabled = True if db_warns == None else False)
                button_bans = Button(label="Bans", disabled = True if db_bans == None else False)
                button_kicks = Button(label="Kicks", disabled = True if db_kicks == None else False)

                async def button_warns_callback(interaction):
                    button_warns_delete = Button(label="Delete", style = disnake.ButtonStyle.red)
                    button_warns_edit = Button(label="Edit")
                    button_warns_exit = Button(label="Exit")
                    button_warn_next = Button(label="Next")
                    buton_warn_previous = Button(label="Previous")

                    if interaction.author.id == ctx.author.id:
                            db_warns = db.child("MODERATIONS").child("WARNS").child(ctx.guild.id).child(user.id).get()

                            db_list = list(db_warns)
                            #print(db_list)
                            db_list.pop()
                            #print(db_list)
                            db_first = db_list[0]
                            warn = db_warns.get(db_first)
                            warn_id = db_first

                            mod_id = warn["moderator"]
                            reason = warn["reason"]
                            time = warn["datetime"]
                            embeds == [
                                warns_embed_1 == disnake.Embed(
                                    title = f"{user.name}\'s Warnings",
                                    color = disnake.Color.dark_red()
                                    ),
                                warns_embed_1 == disnake.Embed(
                                    title = f"{user.name}\'s Warnings",
                                    color = disnake.Color.dark_red()
                                    )  
                            ]
                            embeds.add_field(
                                name = f"{warn_number}/{warn_count}",
                                value = f"Warn ID: ``{warn_id}``\n\n"
                                        f"Mod ID: ``{mod_id}``\n"
                                        f"Mod: <@!{mod_id}>\n\n"
                                        f"Member ID: {user.id}\n"
                                        f"Member: <@!{user.id}>\n"
                                        f"Reason: ``{reason}``\n"
                                        f"At: ``{time}``"
                                )

    @commands.command()
    async def staffteam(self, ctx, option=None, role: disnake.Role=None):
        members = disnake.Member
        admin = get(ctx.guild.roles, id=966478164924710932)
        if option == None:
            staff_help = disnake.Embed(
                title= "Command help",
                description="``k.staffteam [option]``",
                color=disnake.Color.dark_red()
            )

            staff_help.add_field(
                name="Options",
                value="``Update\n"
                      "Open\n"
                      "Remove``\n"
            )
            await ctx.send(embed=staff_help)
        elif option=="open":
            admin_embed = disnake.Embed(
                title="Staff Team",
                color=disnake.Color.dark_red()
            )
            admin_embed.add_field(
                name="Admin",
                value="\n".join(str(member.mention) for member in admin.members)
            )
            await ctx.send(embed=admin_embed)
        else:
            await ctx.send("\n".join(str(member) for member in role.members))

def setup(client):
    client.add_cog(Testing(client))
    print("Cog: Testing - loaded")

def teardown(client):
    print("Cog: Testing - unloaded.")
