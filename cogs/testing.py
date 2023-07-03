import disnake
from disnake.utils import get
from disnake.ext import commands
from disnake.ext.commands import has_permissions, Paginator

from disnake.ui import Button, View

import datetime
from datetime import datetime as dt

import pyrebase
import json
import os

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
        #self.warn_number = 0
        #self.page_number = 0
        self.current_page = 0
        self.pages = {}
        self.pages_list = {}

    @commands.command(aliases=["warns", "check"], pass_context=True)
    async def warnings(self, ctx, user:disnake.User=None):
        if user == None:
            await ctx.send("Please tell me who to check.")
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
                    button_warns_next = Button(label="Next")
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
                                    print("started-previous_previous")
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
                                    print("started-previous")
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
                                    print("started-next_next")
                                    if interaction.author.id == ctx.author.id:
                                        self.current_page += 1
                                        if self.current_page >= page_number:
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
                                    print("started-next")
                                    if interaction.author.id == ctx.author.id:
                                        self.current_page += 1
                                        if self.current_page >= page_number:
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

                async def on_error(self, error, item, interaction):
                    print(error)

                button_warns.callback = button_warns_callback
                #button_bans.callback = button_bans_callback
                #button_kicks.callback = button_kicks_callback

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
                value="Update\n"
                      "Open\n"
                      "Remove\n"
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
