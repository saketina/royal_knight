import datetime
import json
import os
import random
from datetime import datetime as dt
from random import choice

import disnake
import pyrebase
from disnake.ext import commands
from disnake.ext.commands import has_permissions
from disnake.ui import Button, View
from disnake.utils import get
from PIL import Image
from io import BytesIO

# TODO ALL/transfer finished commands to appropriate cogs

firebase = pyrebase.initialize_app(json.load(open("./firebase_config.json", "r")))
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
    async def gif_redo(self, ctx):
        rp = os.listdir("./RP_OLD")
        for command in rp:
            all_gifs = os.listdir(f"./RP_OLD/{command}")
            counter = 0
            for g in all_gifs:
                counter += 1
                """
                gif = Image.open(f"./RP_OLD/{command}/{g}")
                selected_gif = gif.resize((500, 264))
                #gif_bytes = selected_gif.tobytes()
                path = f"./RP/{command}/{command}({counter}).gif"
                selected_gif.save(path, format="GIF", save_all=True)
                """

                gif_image = Image.open(f"./RP_OLD/{command}/{g}")
                image_bytes = BytesIO()
                gif_image.resize((500, 264))
                gif_image.tobytes()
                gif_image.save(image_bytes, format="GIF", save_all=True)
                image_bytes.seek(0)
                #print(image_bytes)
                path = f"./RP/{command}/{command}({counter}).gif"
                #image_bytes.save(path, format="GIF", save_all=True)
                BytesIO.write(gif_image)
                gif_image.close()
        print("done")

    @commands.command()
    async def gif_test(self, ctx):
        cmd = "bite", "blush"#, "bonk", "boop", "cry", "cuddle", "dance", "die", "handhold", "hug", "kill", "kiss", "nom", "pat", "punch", "slap", "smile"
        for item in cmd:
            gifs = os.listdir(f"./RP/{item}/")
            if gifs == []:
                return
            gif_count = 0

            for gif in gifs:
                gif_count += 1
                path_to_gif = f"./RP/{item}/{gif}"
                file = disnake.File(path_to_gif, filename="gif.gif")

                kiss_embed = disnake.Embed(
                    title="",
                    description=f"{item} {gif_count}",
                )
                kiss_embed.set_image(url="attachment://gif.gif")
                await ctx.send(embed=kiss_embed, file=file)

    """
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member:disnake.Member=None, duration=None, *, reason=None):
        # TODO MUTE/add checks if the member is muted or not
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
                # TODO MUTE_ROLE add a way to dynamically set the role to db
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
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member:disnake.Member=None):
        # TODO UNMUTE/add checks if the member is muted or not
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
    """
    @commands.command(aliases=["warns", "check", "moderations"], pass_context=True)
    async def warnings(self, ctx, user:disnake.User=None):
        try:
            self.pages_list.popitem(user.id)
        except:
            pass
        if user == None:
            embed = disnake.Embed(
                title = "WARNINGS COMMAND",
                description = "``k.moderations [@user/user id]``",
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
                    button_warns_delete = Button(emoji="🚮", style = disnake.ButtonStyle.red)
                    button_warns_edit = Button(emoji="✏")
                    button_warns_exit = Button(emoji="❌")
                    button_warns_next = Button(emoji="➡", disabled = False)
                    button_warns_previous = Button(emoji="⬅", disabled=True)
                    button_warns_proof = Button(emoji="📷")

                    if author_check(ctx, interaction):
                            moderation = db.child("MODERATIONS").child("WARNS").child(ctx.guild.id).child(user.id).get().val()
                            #print(moderation)
                            if db_warns != None:
                                moderation.popitem(str("warns"))

                                #self.warn_number[user.id] = 0
                                warn_number = 0
                                #self.page_number[user.id] = 0
                                page_number = 0
                                self.pages = {}
                                pages_num = []
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
                                    embed.set_image(url=warn["proof"])

                                    page_number += 1
                                    self.pages[page_number] = embed

                                    pages_num.append(key)
                                    
                                self.pages_list[user.id] = self.pages
                                #print(moderation)
                                pages = self.pages_list[user.id]
                                #print(pages_num)
                                number = moderation.popitem(last=False)

                                self.current_page = 1

                                async def button_warns_proof_callback(interaction):
                                    if interaction.author.id == ctx.author.id:
                                        MyView.message = await interaction.response.edit_message(view=None)
                                        await ctx.send("Please attach an image after this message.")
                                        def check(m):
                                            return m.author == ctx.author and m.channel == ctx.channel
                                        msg = await self.client.wait_for("message", check=check)
                                        temp = msg.attachments
                                        num = self.current_page - 1 
                                        db.child("MODERATIONS").child("WARNS").child(ctx.guild.id).child(user.id).child(pages_num[num]).update({"proof": str(temp[0])})

                                        await ctx.send(content="The attachment has been saved")
                                
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
                                        embed.set_image(url=warn["proof"])

                                        #edit_embed.set_footer(text = {dt.now()})

                                        db.child("MODERATIONS").child("WARNS").child(ctx.guild.id).child(user.id).child(self.current_page).update({"reason": str(msg.content)})
                                        await ctx.send(f"The reason has been changed to ``{msg.content}``.")
                                        await interaction.edit_original_response(view = None)

                                async def button_warns_delete_callback(interaction):
                                    if interaction.author.id == ctx.author.id:
                                        button_warns_yes = Button(emoji="✅", style=disnake.ButtonStyle.green)
                                        button_warns_no = Button(emoji="❌", style=disnake.ButtonStyle.red)

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
                                            button_warns_previous = Button(emoji="⬅", disabled=True)
                                        else:
                                            button_warns_previous = Button(emoji="⬅", disabled=False)

                                        button_warns_previous.callback=button_warns_previous_callback
                                        
                                        view = MyView(timeout=30, interaction=[button_warns_proof_callback, button_warns_delete_callback, button_warns_edit_callback, button_warns_exit_callback, button_warns_next_callback, button_warns_previous_callback])
                                        view.add_item(button_warns_previous)
                                        view.add_item(button_warns_delete)
                                        view.add_item(button_warns_edit)
                                        view.add_item(button_warns_proof)
                                        view.add_item(button_warns_exit)
                                        view.add_item(button_warns_next)
                                        MyView.message = await interaction.response.edit_message(embed=pages[self.current_page], view=view)
                            
                                async def button_warns_previous_callback(interaction):
                                    # print("started-previous")
                                    if interaction.author.id == ctx.author.id:
                                        self.current_page -= 1

                                        if self.current_page == 1:
                                            button_warns_previous = Button(emoji="⬅", disabled=True)
                                        else:
                                            button_warns_previous = Button(emoji="⬅", disabled=False)

                                        button_warns_previous.callback=button_warns_previous_previous_callback
                                        
                                        view = MyView(timeout=30, interaction=[button_warns_proof_callback, button_warns_delete_callback, button_warns_edit_callback, button_warns_exit_callback, button_warns_next_next_callback, button_warns_previous_previous_callback])
                                        view.add_item(button_warns_previous)
                                        view.add_item(button_warns_delete)
                                        view.add_item(button_warns_edit)
                                        view.add_item(button_warns_proof)
                                        view.add_item(button_warns_exit)
                                        view.add_item(button_warns_next)
                                        MyView.message = await interaction.response.edit_message(embed=pages[self.current_page], view=view)
                            
                                async def button_warns_next_next_callback(interaction):
                                    # print("started-next_next")
                                    if interaction.author.id == ctx.author.id:
                                        self.current_page += 1

                                        if self.current_page == page_number:
                                            button_warns_next = Button(emoji="➡", disabled=True)
                                        elif self.current_page >= page_number:
                                            button_warns_next = Button(emoji="➡", disabled=True)
                                        else:
                                            button_warns_next = Button(emoji="➡", disabled=False)

                                        if self.current_page == 1:
                                            button_warns_previous = Button(emoji="⬅", disabled=True)
                                        else:
                                            button_warns_previous = Button(emoji="⬅", disabled=False)

                                        button_warns_next.callback=button_warns_next_callback
                                        button_warns_previous.callback=button_warns_previous_previous_callback
                                        
                                        view = MyView(timeout=30, interaction=[button_warns_proof_callback, button_warns_delete_callback, button_warns_edit_callback, button_warns_exit_callback, button_warns_next_callback, button_warns_previous_previous_callback])
                                        view.add_item(button_warns_previous)
                                        view.add_item(button_warns_delete)
                                        view.add_item(button_warns_edit)
                                        view.add_item(button_warns_proof)
                                        view.add_item(button_warns_exit)
                                        view.add_item(button_warns_next)
                                        MyView.message = await interaction.response.edit_message(embed=pages[self.current_page], view=view)
                                
                                async def button_warns_next_callback(interaction):
                                    # print("started-next")
                                    if interaction.author.id == ctx.author.id:
                                        self.current_page += 1

                                        if self.current_page == page_number:
                                            button_warns_next = Button(emoji="➡", disabled=True)
                                        elif self.current_page >= page_number:
                                            button_warns_next = Button(emoji="➡", disabled=True)
                                        else:
                                            button_warns_next = Button(emoji="➡", disabled=False)
                                        
                                        if self.current_page == 1:
                                            button_warns_previous = Button(emoji="⬅", disabled=True)
                                        else:
                                            button_warns_previous = Button(emoji="⬅", disabled=False)

                                        button_warns_next.callback=button_warns_next_next_callback
                                        button_warns_previous.callback=button_warns_previous_previous_callback
                                        
                                        view = MyView(timeout=30, interaction=[button_warns_proof_callback, button_warns_delete_callback, button_warns_edit_callback, button_warns_exit_callback, button_warns_next_next_callback, button_warns_previous_previous_callback])
                                        view.add_item(button_warns_previous)
                                        view.add_item(button_warns_delete)
                                        view.add_item(button_warns_edit)
                                        view.add_item(button_warns_proof)
                                        view.add_item(button_warns_exit)
                                        view.add_item(button_warns_next)
                                        MyView.message = await interaction.response.edit_message(embed=pages[self.current_page], view=view)

                                if self.current_page == page_number:
                                            button_warns_next = Button(emoji="➡", disabled=True)
                                elif self.current_page >= page_number:
                                    button_warns_next = Button(emoji="➡", disabled=True)
                                else:
                                    button_warns_next = Button(emoji="➡", disabled=False)

                                button_warns_delete.callback = button_warns_delete_callback
                                button_warns_edit.callback = button_warns_edit_callback
                                button_warns_exit.callback = button_warns_exit_callback
                                button_warns_proof.callback = button_warns_proof_callback
                                button_warns_next.callback = button_warns_next_callback
                                button_warns_previous.callback = button_warns_previous_callback

                                view_warns = MyView(timeout=30, interaction=[button_warns_delete_callback, button_warns_edit_callback, button_warns_proof_callback, button_warns_exit_callback, button_warns_previous_callback, button_warns_next_callback])
                                view_warns.add_item(button_warns_previous)
                                view_warns.add_item(button_warns_delete)
                                view_warns.add_item(button_warns_edit)
                                view_warns.add_item(button_warns_proof)
                                view_warns.add_item(button_warns_exit)
                                view_warns.add_item(button_warns_next)
                                MyView.message = await interaction.response.edit_message(embed=pages[1], view=view_warns)
                                async def on_error(self, error, item, interaction):
                                    print(error)
                            else:
                                print("There aren't any moderations")

                    else:
                        return

                async def button_bans_callback(interaction):
                    button_bans_delete = Button(emoji="🚮", style = disnake.ButtonStyle.red)
                    button_bans_edit = Button(emoji="✏")
                    button_bans_exit = Button(emoji="❌")
                    button_bans_next = Button(emoji="➡", disabled = False)
                    button_bans_previous = Button(emoji="⬅", disabled=True)
                    button_bans_proof = Button(emoji="📷")

                    if author_check(ctx, interaction):
                            moderation = db.child("MODERATIONS").child("BANS").child(ctx.guild.id).child(user.id).get().val()
                            #print(moderation)
                            if db_bans != None:
                                moderation.popitem(str("bans"))

                                #self.ban_number[user.id] = 0
                                ban_number = 0
                                #self.page_number[user.id] = 0
                                page_number = 0
                                self.pages = {}
                                pages_num = []
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
                                    value = f"Warn ID: ``{ban_id}``\n\n"
                                            f"Mod ID: ``{mod_id}``\n"
                                            f"Mod: <@!{mod_id}>\n\n"
                                            f"Member ID: {user.id}\n"
                                            f"Member: <@!{user.id}>\n"
                                            f"Reason: ``{reason}``\n"
                                            f"At: ``{time}``"
                                    )

                                    embed.set_image(url=ban["proof"])

                                    page_number += 1
                                    self.pages[page_number] = embed

                                    pages_num.append(key)
                                    
                                self.pages_list[user.id] = self.pages
                                #print(moderation)
                                pages = self.pages_list[user.id]
                                #print(pages_num)
                                number = moderation.popitem(last=False)

                                self.current_page = 1

                                async def button_bans_proof_callback(interaction):
                                    if interaction.author.id == ctx.author.id:
                                        MyView.message = await interaction.response.edit_message(view=None)
                                        await ctx.send("Please attach an image after this message.")
                                        def check(m):
                                            return m.author == ctx.author and m.channel == ctx.channel
                                        msg = await self.client.wait_for("message", check=check)
                                        temp = msg.attachments
                                        num = self.current_page - 1 
                                        db.child("MODERATIONS").child("BANS").child(ctx.guild.id).child(user.id).child(pages_num[num]).update({"proof": str(temp[0])})

                                        await ctx.send(content="The attachment has been saved")
                                
                                async def button_bans_edit_callback(interaction):
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

                                        mod_id = ban["moderator"]
                                        time = ban["datetime"]

                                        edit_embed.add_field(
                                            name = f"{ban_number}/{ban_count}",
                                            value = f"Warn ID: ``{ban_id}``\n\n"
                                                    f"Mod ID: ``{mod_id}``\n"
                                                    f"Mod: <@!{mod_id}>\n\n"
                                                    f"Member ID: {user.id}\n"
                                                    f"Member: <@!{user.id}>\n"
                                                    f"Reason: ``{msg.content}``\n"
                                                    f"At: ``{time}``"
                                                    )
                                        embed.set_image(url=ban["proof"])

                                        #edit_embed.set_footer(text = {dt.now()})

                                        db.child("MODERATIONS").child("BANS").child(ctx.guild.id).child(user.id).child(self.current_page).update({"reason": str(msg.content)})
                                        await ctx.send(f"The reason has been changed to ``{msg.content}``.")
                                        await interaction.edit_original_response(view = None)

                                async def button_bans_delete_callback(interaction):
                                    if interaction.author.id == ctx.author.id:
                                        button_bans_yes = Button(emoji="✅", style=disnake.ButtonStyle.green)
                                        button_bans_no = Button(emoji="❌", style=disnake.ButtonStyle.red)

                                        async def button_bans_yes_callback(interaction):
                                            if interaction.author.id == ctx.author.id:
                                                await interaction.response.defer(with_message = False)
                                                db.child("MODERATIONS").child("BANS").child(ctx.guild.id).child(user.id).child(self.current_page).remove()
                                                await interaction.edit_original_response(content="The ban has been deleted 🚮", view=None)
                                            else:
                                                return

                                        async def button_bans_no_callback(interaction):
                                            if interaction.author.id == ctx.author.id:
                                                await interaction.response.edit_message(content="I didn\'t delete any ban", view=None)
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
                                            button_bans_previous = Button(emoji="⬅", disabled=True)
                                        else:
                                            button_bans_previous = Button(emoji="⬅", disabled=False)

                                        button_bans_previous.callback=button_bans_previous_callback
                                        
                                        view = MyView(timeout=30, interaction=[button_bans_proof_callback, button_bans_delete_callback, button_bans_edit_callback, button_bans_exit_callback, button_bans_next_callback, button_bans_previous_callback])
                                        view.add_item(button_bans_previous)
                                        view.add_item(button_bans_delete)
                                        view.add_item(button_bans_edit)
                                        view.add_item(button_bans_proof)
                                        view.add_item(button_bans_exit)
                                        view.add_item(button_bans_next)
                                        MyView.message = await interaction.response.edit_message(embed=pages[self.current_page], view=view)
                            
                                async def button_bans_previous_callback(interaction):
                                    # print("started-previous")
                                    if interaction.author.id == ctx.author.id:
                                        self.current_page -= 1

                                        if self.current_page == 1:
                                            button_bans_previous = Button(emoji="⬅", disabled=True)
                                        else:
                                            button_bans_previous = Button(emoji="⬅", disabled=False)

                                        button_bans_previous.callback=button_bans_previous_previous_callback
                                        
                                        view = MyView(timeout=30, interaction=[button_bans_proof_callback, button_bans_delete_callback, button_bans_edit_callback, button_bans_exit_callback, button_bans_next_next_callback, button_bans_previous_previous_callback])
                                        view.add_item(button_bans_previous)
                                        view.add_item(button_bans_delete)
                                        view.add_item(button_bans_edit)
                                        view.add_item(button_bans_proof)
                                        view.add_item(button_bans_exit)
                                        view.add_item(button_bans_next)
                                        MyView.message = await interaction.response.edit_message(embed=pages[self.current_page], view=view)
                            
                                async def button_bans_next_next_callback(interaction):
                                    # print("started-next_next")
                                    if interaction.author.id == ctx.author.id:
                                        self.current_page += 1

                                        if self.current_page == page_number:
                                            button_bans_next = Button(emoji="➡", disabled=True)
                                        elif self.current_page >= page_number:
                                            button_bans_next = Button(emoji="➡", disabled=True)
                                        else:
                                            button_bans_next = Button(emoji="➡", disabled=False)

                                        if self.current_page == 1:
                                            button_bans_previous = Button(emoji="⬅", disabled=True)
                                        else:
                                            button_bans_previous = Button(emoji="⬅", disabled=False)

                                        button_bans_next.callback=button_bans_next_callback
                                        button_bans_previous.callback=button_bans_previous_previous_callback
                                        
                                        view = MyView(timeout=30, interaction=[button_bans_proof_callback, button_bans_delete_callback, button_bans_edit_callback, button_bans_exit_callback, button_bans_next_callback, button_bans_previous_previous_callback])
                                        view.add_item(button_bans_previous)
                                        view.add_item(button_bans_delete)
                                        view.add_item(button_bans_edit)
                                        view.add_item(button_bans_proof)
                                        view.add_item(button_bans_exit)
                                        view.add_item(button_bans_next)
                                        MyView.message = await interaction.response.edit_message(embed=pages[self.current_page], view=view)
                                
                                async def button_bans_next_callback(interaction):
                                    # print("started-next")
                                    if interaction.author.id == ctx.author.id:
                                        self.current_page += 1

                                        if self.current_page == page_number:
                                            button_bans_next = Button(emoji="➡", disabled=True)
                                        elif self.current_page >= page_number:
                                            button_bans_next = Button(emoji="➡", disabled=True)
                                        else:
                                            button_bans_next = Button(emoji="➡", disabled=False)
                                        
                                        if self.current_page == 1:
                                            button_bans_previous = Button(emoji="⬅", disabled=True)
                                        else:
                                            button_bans_previous = Button(emoji="⬅", disabled=False)

                                        button_bans_next.callback=button_bans_next_next_callback
                                        button_bans_previous.callback=button_bans_previous_previous_callback
                                        
                                        view = MyView(timeout=30, interaction=[button_bans_proof_callback, button_bans_delete_callback, button_bans_edit_callback, button_bans_exit_callback, button_bans_next_next_callback, button_bans_previous_previous_callback])
                                        view.add_item(button_bans_previous)
                                        view.add_item(button_bans_delete)
                                        view.add_item(button_bans_edit)
                                        view.add_item(button_bans_proof)
                                        view.add_item(button_bans_exit)
                                        view.add_item(button_bans_next)
                                        MyView.message = await interaction.response.edit_message(embed=pages[self.current_page], view=view)

                                if self.current_page == page_number:
                                            button_bans_next = Button(emoji="➡", disabled=True)
                                elif self.current_page >= page_number:
                                    button_bans_next = Button(emoji="➡", disabled=True)
                                else:
                                    button_bans_next = Button(emoji="➡", disabled=False)

                                button_bans_delete.callback = button_bans_delete_callback
                                button_bans_edit.callback = button_bans_edit_callback
                                button_bans_exit.callback = button_bans_exit_callback
                                button_bans_proof.callback = button_bans_proof_callback
                                button_bans_next.callback = button_bans_next_callback
                                button_bans_previous.callback = button_bans_previous_callback

                                view_bans = MyView(timeout=30, interaction=[button_bans_delete_callback, button_bans_edit_callback, button_bans_proof_callback, button_bans_exit_callback, button_bans_previous_callback, button_bans_next_callback])
                                view_bans.add_item(button_bans_previous)
                                view_bans.add_item(button_bans_delete)
                                view_bans.add_item(button_bans_edit)
                                view_bans.add_item(button_bans_proof)
                                view_bans.add_item(button_bans_exit)
                                view_bans.add_item(button_bans_next)
                                MyView.message = await interaction.response.edit_message(embed=pages[1], view=view_bans)
                                async def on_error(self, error, item, interaction):
                                    print(error)
                            else:
                                print("There aren't any moderations")

                    else:
                        return

                async def button_kicks_callback(interaction):
                    button_kicks_delete = Button(emoji="🚮", style = disnake.ButtonStyle.red)
                    button_kicks_edit = Button(emoji="✏")
                    button_kicks_exit = Button(emoji="❌")
                    button_kicks_next = Button(emoji="➡", disabled = False)
                    button_kicks_previous = Button(emoji="⬅", disabled=True)
                    button_kicks_proof = Button(emoji="📷")

                    if author_check(ctx, interaction):
                            moderation = db.child("MODERATIONS").child("KICKS").child(ctx.guild.id).child(user.id).get().val()
                            #print(moderation)
                            if db_kicks != None:
                                moderation.popitem(str("kicks"))

                                #self.kick_number[user.id] = 0
                                kick_number = 0
                                #self.page_number[user.id] = 0
                                page_number = 0
                                self.pages = {}
                                pages_num = []
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
                                        title=f"{user.name}\'s Warnings",
                                        color=disnake.Color.dark_red()
                                    )
                                    embed.add_field(
                                    name = f"{kick_number}/{kick_count}",
                                    value = f"Warn ID: ``{kick_id}``\n\n"
                                            f"Mod ID: ``{mod_id}``\n"
                                            f"Mod: <@!{mod_id}>\n\n"
                                            f"Member ID: {user.id}\n"
                                            f"Member: <@!{user.id}>\n"
                                            f"Reason: ``{reason}``\n"
                                            f"At: ``{time}``"
                                    )
                                    embed.set_image(url=kick["proof"])

                                    page_number += 1
                                    self.pages[page_number] = embed

                                    pages_num.append(key)
                                    
                                self.pages_list[user.id] = self.pages
                                #print(moderation)
                                pages = self.pages_list[user.id]
                                #print(pages_num)
                                number = moderation.popitem(last=False)

                                self.current_page = 1

                                async def button_kicks_proof_callback(interaction):
                                    if interaction.author.id == ctx.author.id:
                                        MyView.message = await interaction.response.edit_message(view=None)
                                        await ctx.send("Please attach an image after this message.")
                                        def check(m):
                                            return m.author == ctx.author and m.channel == ctx.channel
                                        msg = await self.client.wait_for("message", check=check)
                                        temp = msg.attachments
                                        num = self.current_page - 1 
                                        db.child("MODERATIONS").child("KICKS").child(ctx.guild.id).child(user.id).child(pages_num[num]).update({"proof": str(temp[0])})

                                        await ctx.send(content="The attachment has been saved")
                                
                                async def button_kicks_edit_callback(interaction):
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

                                        mod_id = kick["moderator"]
                                        time = kick["datetime"]

                                        edit_embed.add_field(
                                            name = f"{kick_number}/{kick_count}",
                                            value = f"Warn ID: ``{kick_id}``\n\n"
                                                    f"Mod ID: ``{mod_id}``\n"
                                                    f"Mod: <@!{mod_id}>\n\n"
                                                    f"Member ID: {user.id}\n"
                                                    f"Member: <@!{user.id}>\n"
                                                    f"Reason: ``{msg.content}``\n"
                                                    f"At: ``{time}``"
                                                    )
                                        embed.set_image(url=kick["proof"])

                                        #edit_embed.set_footer(text = {dt.now()})

                                        db.child("MODERATIONS").child("KICKS").child(ctx.guild.id).child(user.id).child(self.current_page).update({"reason": str(msg.content)})
                                        await ctx.send(f"The reason has been changed to ``{msg.content}``.")
                                        await interaction.edit_original_response(view = None)

                                async def button_kicks_delete_callback(interaction):
                                    if interaction.author.id == ctx.author.id:
                                        button_kicks_yes = Button(emoji="✅", style=disnake.ButtonStyle.green)
                                        button_kicks_no = Button(emoji="❌", style=disnake.ButtonStyle.red)

                                        async def button_kicks_yes_callback(interaction):
                                            if interaction.author.id == ctx.author.id:
                                                await interaction.response.defer(with_message = False)
                                                db.child("MODERATIONS").child("KICKS").child(ctx.guild.id).child(user.id).child(self.current_page).remove()
                                                await interaction.edit_original_response(content="The kick has been deleted 🚮", view=None)
                                            else:
                                                return

                                        async def button_kicks_no_callback(interaction):
                                            if interaction.author.id == ctx.author.id:
                                                await interaction.response.edit_message(content="I didn\'t delete any kick", view=None)
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
                                            button_kicks_previous = Button(emoji="⬅", disabled=True)
                                        else:
                                            button_kicks_previous = Button(emoji="⬅", disabled=False)

                                        button_kicks_previous.callback=button_kicks_previous_callback
                                        
                                        view = MyView(timeout=30, interaction=[button_kicks_proof_callback, button_kicks_delete_callback, button_kicks_edit_callback, button_kicks_exit_callback, button_kicks_next_callback, button_kicks_previous_callback])
                                        view.add_item(button_kicks_previous)
                                        view.add_item(button_kicks_delete)
                                        view.add_item(button_kicks_edit)
                                        view.add_item(button_kicks_proof)
                                        view.add_item(button_kicks_exit)
                                        view.add_item(button_kicks_next)
                                        MyView.message = await interaction.response.edit_message(embed=pages[self.current_page], view=view)
                            
                                async def button_kicks_previous_callback(interaction):
                                    # print("started-previous")
                                    if interaction.author.id == ctx.author.id:
                                        self.current_page -= 1

                                        if self.current_page == 1:
                                            button_kicks_previous = Button(emoji="⬅", disabled=True)
                                        else:
                                            button_kicks_previous = Button(emoji="⬅", disabled=False)

                                        button_kicks_previous.callback=button_kicks_previous_previous_callback
                                        
                                        view = MyView(timeout=30, interaction=[button_kicks_proof_callback, button_kicks_delete_callback, button_kicks_edit_callback, button_kicks_exit_callback, button_kicks_next_next_callback, button_kicks_previous_previous_callback])
                                        view.add_item(button_kicks_previous)
                                        view.add_item(button_kicks_delete)
                                        view.add_item(button_kicks_edit)
                                        view.add_item(button_kicks_proof)
                                        view.add_item(button_kicks_exit)
                                        view.add_item(button_kicks_next)
                                        MyView.message = await interaction.response.edit_message(embed=pages[self.current_page], view=view)
                            
                                async def button_kicks_next_next_callback(interaction):
                                    # print("started-next_next")
                                    if interaction.author.id == ctx.author.id:
                                        self.current_page += 1

                                        if self.current_page == page_number:
                                            button_kicks_next = Button(emoji="➡", disabled=True)
                                        elif self.current_page >= page_number:
                                            button_kicks_next = Button(emoji="➡", disabled=True)
                                        else:
                                            button_kicks_next = Button(emoji="➡", disabled=False)

                                        if self.current_page == 1:
                                            button_kicks_previous = Button(emoji="⬅", disabled=True)
                                        else:
                                            button_kicks_previous = Button(emoji="⬅", disabled=False)

                                        button_kicks_next.callback=button_kicks_next_callback
                                        button_kicks_previous.callback=button_kicks_previous_previous_callback
                                        
                                        view = MyView(timeout=30, interaction=[button_kicks_proof_callback, button_kicks_delete_callback, button_kicks_edit_callback, button_kicks_exit_callback, button_kicks_next_callback, button_kicks_previous_previous_callback])
                                        view.add_item(button_kicks_previous)
                                        view.add_item(button_kicks_delete)
                                        view.add_item(button_kicks_edit)
                                        view.add_item(button_kicks_proof)
                                        view.add_item(button_kicks_exit)
                                        view.add_item(button_kicks_next)
                                        MyView.message = await interaction.response.edit_message(embed=pages[self.current_page], view=view)
                                
                                async def button_kicks_next_callback(interaction):
                                    # print("started-next")
                                    if interaction.author.id == ctx.author.id:
                                        self.current_page += 1

                                        if self.current_page == page_number:
                                            button_kicks_next = Button(emoji="➡", disabled=True)
                                        elif self.current_page >= page_number:
                                            button_kicks_next = Button(emoji="➡", disabled=True)
                                        else:
                                            button_kicks_next = Button(emoji="➡", disabled=False)
                                        
                                        if self.current_page == 1:
                                            button_kicks_previous = Button(emoji="⬅", disabled=True)
                                        else:
                                            button_kicks_previous = Button(emoji="⬅", disabled=False)

                                        button_kicks_next.callback=button_kicks_next_next_callback
                                        button_kicks_previous.callback=button_kicks_previous_previous_callback
                                        
                                        view = MyView(timeout=30, interaction=[button_kicks_proof_callback, button_kicks_delete_callback, button_kicks_edit_callback, button_kicks_exit_callback, button_kicks_next_next_callback, button_kicks_previous_previous_callback])
                                        view.add_item(button_kicks_previous)
                                        view.add_item(button_kicks_delete)
                                        view.add_item(button_kicks_edit)
                                        view.add_item(button_kicks_proof)
                                        view.add_item(button_kicks_exit)
                                        view.add_item(button_kicks_next)
                                        MyView.message = await interaction.response.edit_message(embed=pages[self.current_page], view=view)

                                if self.current_page == page_number:
                                            button_kicks_next = Button(emoji="➡", disabled=True)
                                elif self.current_page >= page_number:
                                    button_kicks_next = Button(emoji="➡", disabled=True)
                                else:
                                    button_kicks_next = Button(emoji="➡", disabled=False)

                                button_kicks_delete.callback = button_kicks_delete_callback
                                button_kicks_edit.callback = button_kicks_edit_callback
                                button_kicks_exit.callback = button_kicks_exit_callback
                                button_kicks_proof.callback = button_kicks_proof_callback
                                button_kicks_next.callback = button_kicks_next_callback
                                button_kicks_previous.callback = button_kicks_previous_callback

                                view_kicks = MyView(timeout=30, interaction=[button_kicks_delete_callback, button_kicks_edit_callback, button_kicks_proof_callback, button_kicks_exit_callback, button_kicks_previous_callback, button_kicks_next_callback])
                                view_kicks.add_item(button_kicks_previous)
                                view_kicks.add_item(button_kicks_delete)
                                view_kicks.add_item(button_kicks_edit)
                                view_kicks.add_item(button_kicks_proof)
                                view_kicks.add_item(button_kicks_exit)
                                view_kicks.add_item(button_kicks_next)
                                MyView.message = await interaction.response.edit_message(embed=pages[1], view=view_kicks)
                                async def on_error(self, error, item, interaction):
                                    print(error)
                            else:
                                print("There aren't any moderations")

                    else:
                        return
                
                async def on_error(self, error, item, interaction):
                    print(error)

                button_warns.callback = button_warns_callback
                button_bans.callback = button_bans_callback
                button_kicks.callback = button_kicks_callback

                view_select = MyView(timeout=30, interaction=[button_warns_callback, button_bans_callback, button_kicks_callback])

                view_select.add_item(button_warns)
                view_select.add_item(button_bans)
                view_select.add_item(button_kicks)

                MyView.message = await ctx.send(embed=warnings_embed, view=view_select)
            else:
                await ctx.send("I see no moderations")

    @commands.command()
    ## TODO FEATURE-ADD staff: create, promote, update, demote
    ## TODO link to database
    async def staff(self, ctx, option=None):
        auth_roles = []
        for role in ctx.author.roles:
            auth_roles.append(role.id)

        if 706162869783363725 not in auth_roles:
            return
        else:
            ## staff profile here
            embed = disnake.Embed(
                title= f"{ctx.author.nick}'s staff profile",
                color=disnake.Color.dark_red()
            )
            embed.add_field(
                name="Staff info",
                value="Staff since: forever"
            )
            embed.set_author(
                name=ctx.author.nick,
                icon_url=ctx.author.avatar
            )
            await ctx.send(embed=embed)
    
    @commands.command()
    async def staffteam(self, ctx, option=None):
        members = disnake.Member
        role = ctx.guild.get_role(706162869783363725)
        role_list = [
            ctx.guild.get_role(706540593865556071), ## owner
            ctx.guild.get_role(687228928565444800), ## co-owner
            ctx.guild.get_role(706161806426767470), ## admin
            ctx.guild.get_role(801614132771160095), ## head mod
            ctx.guild.get_role(747680315257913384), ## mod
            ctx.guild.get_role(870431101955493999), ## trial
        ]
        #print(role_list)
        
        if option == None:
            def returnNotMatches(a, b):
                temp=[]
                for x in a:
                    if x in b:
                        pass
                    else:
                        temp.append(x)
                return temp
            embed = disnake.Embed(
                title="Staff Team",
                color=disnake.Color.dark_red()
            )
            embed.add_field(
                name="Owners",
                value="\n".join(str(member.mention) for member in role_list[0].members),
                inline=False
            )
            embed.add_field(
                name="Co-Owners",
                value="\n".join(str(member.mention) for member in returnNotMatches(role_list[1].members, role_list[0].members)),
                inline=False
            )
            embed.add_field(
                name="Admins",
                value="\n".join(str(member.mention) for member in returnNotMatches(role_list[2].members, role_list[1].members)),
                inline=False
            )
            embed.add_field(
                name="Head moderators",
                value="\n".join(str(member.mention) for member in returnNotMatches(role_list[3].members, role_list[2].members)),
                inline=False
            )
            embed.add_field(
                name="Moderators",
                value="\n".join(str(member.mention) for member in returnNotMatches(role_list[4].members, role_list[3].members)),
                inline=False
            )
            embed.add_field(
                name="Trial moderators",
                value="\n".join(str(member.mention) for member in returnNotMatches(role_list[5].members, role_list[4].members)),
                inline=False
            )
            await ctx.send(embed=embed)
            
        elif option=="help":
            staff_help = disnake.Embed(
                title= "Command help",
                description="``k.staffteam [option]``",
                color=disnake.Color.dark_red()
            )
            staff_help.add_field(
                name="Options",
                value="``help\nowners\nco-owners\nadmins\nhmods\nmods\ntrials``"
            )
            await ctx.send(embed=staff_help)
        elif option=="owners":
            embed = disnake.Embed(
                title="Staff Team",
                color=disnake.Color.dark_red()
            )
            embed.add_field(
                name="Owners",
                value="\n".join(str(member.mention) for member in role_list[0].members),
                inline=False
            )
        elif option=="co-owners":
            embed = disnake.Embed(
                title="Staff Team",
                color=disnake.Color.dark_red()
            )
            embed.add_field(
                name="Co-Owners",
                value="\n".join(str(member.mention) for member in role_list[1].members),
                inline=False
            )
        elif option=="admins":
            embed = disnake.Embed(
                title="Staff Team",
                color=disnake.Color.dark_red()
            )
            embed.add_field(
                name="Admins",
                value="\n".join(str(member.mention) for member in role_list[2].members),
                inline=False
            )
        elif option=="hmods":
            embed = disnake.Embed(
                title="Staff Team",
                color=disnake.Color.dark_red()
            )
            embed.add_field(
                name="Head Moderators",
                value="\n".join(str(member.mention) for member in role_list[3].members),
                inline=False
            )
        elif option=="mods":
            embed = disnake.Embed(
                title="Staff Team",
                color=disnake.Color.dark_red()
            )
            embed.add_field(
                name="Moderators",
                value="\n".join(str(member.mention) for member in role_list[4].members),
                inline=False
            )
        elif option=="trials":
            embed = disnake.Embed(
                title="Staff Team",
                color=disnake.Color.dark_red()
            )
            embed.add_field(
                name="Trial Moderators",
                value="\n".join(str(member.mention) for member in role_list[0].members),
                inline=False
            )
        else:
            staff_help = disnake.Embed(
                title= "Command help",
                description="``k.staffteam [option]``",
                color=disnake.Color.dark_red()
            )
            staff_help.add_field(
                name="Options",
                value="``help\nowners\nco-owners\nadmins\nhmods\nmods\ntrials``"
            )
            await ctx.send(embed=staff_help)
    
def setup(client):
    client.add_cog(Testing(client))
    print("Cog: Testing - loaded")

def teardown(client):
    print("Cog: Testing - unloaded.")
