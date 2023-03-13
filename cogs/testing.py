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

    @commands.command(aliases=["warns", "check"], pass_context=True)
    async def warnings(self, ctx, user:disnake.User=None):
        if user == None:
            await ctx.send("Please tell me who to check.")
        else:
            db_warns = db.child("MODERATIONS").child("WARNS").child(ctx.guild.id).child(user.id).get().val()
            db_bans = db.child("MODERATIONS").child("BANS").child(ctx.guild.id).child(user.id).get()
            db_kicks = db.child("MODERATIONS").child("KICKS").child(ctx.guild.id).child(user.id).get()
            db_moderations = [db_warns.val(), db_bans.val(), db_kicks.val()]
            #print(db_moderations)
            
            #if db_warns != None:
            #print(db_warns)
            #delattr(db_warns, "warns")
            """
            if db_bans != None:
                db_bans.pop("bans")
            if db_kicks != None:
                db_kicks.pop("kicks")
            """
            #print(db_moderations)
            if db_moderations != [None, None, None]:
                warnings_embed = disnake.Embed(
                    title = f"{user.name}\'s moderations",
                    description = "1. Warns\n2. Bans\n3. Kicks",
                    color = disnake.Color.dark_red()
                )
                #db_warns.pop("warns")
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
                            db_warns = db.child("MODERATIONS").child("WARNS").child(ctx.guild.id).child(user.id).get().val()
                            if db_warns != None:
                                warn_count = len(db_warns) - 1
                                warn_number = 1

                                db_list = list(db_warns)
                                #print(db_list)
                                db_list.pop()
                                #print(db_list)
                                db_first = db_list[0]
                                warn = db_warns.get(db_first)
                                warn_id = db_first

                                warns_embed = disnake.Embed(
                                    title = f"{user.name}\'s Warnings",
                                    color = disnake.Color.dark_red()
                                    )

                                mod_id = warn["moderator"]
                                reason = warn["reason"]
                                time = warn["datetime"]

                                warns_embed.add_field(
                                name = f"{warn_number}/{warn_count}",
                                value = f"Warn ID: ``{warn_id}``\n\n"
                                        f"Mod ID: ``{mod_id}``\n"
                                        f"Mod: <@!{mod_id}>\n\n"
                                        f"Member ID: {user.id}\n"
                                        f"Member: <@!{user.id}>\n"
                                        f"Reason: ``{reason}``\n"
                                        f"At: ``{time}``"
                                        )

                                #warns_embed.set_footer(datetime.datetime.now())

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

                                        db.child("MODERATIONS").child("WARNS").child(ctx.guild.id).child(user.id).child(warn_id).update({"reason": str(msg.content)})
                                        await ctx.send("The moderation has been changed.")
                                        await interaction.edit_original_response(embed = edit_embed, view = None)

                                async def button_warns_delete_callback(interaction):
                                    if interaction.author.id == ctx.author.id:
                                        button_warns_yes = Button(label="Yes", style=disnake.ButtonStyle.green)
                                        button_warns_no = Button(label="No", style=disnake.ButtonStyle.red)

                                    async def button_warns_yes_callback(interaction):
                                        if interaction.author.id == ctx.author.id:
                                            await interaction.response.defer(with_message = False)
                                            db.child("MODERATIONS").child("WARNS").child(ctx.guild.id).child(user.id).child(warn_id).remove()
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

                                button_warns_delete.callback = button_warns_delete_callback
                                button_warns_edit.callback = button_warns_edit_callback

                                view_warns = MyView(timeout=30, interaction=[button_warns_delete_callback, button_warns_edit_callback])
                                view_warns.add_item(button_warns_delete)
                                view_warns.add_item(button_warns_edit)
                                MyView.message = await interaction.response.edit_message(embed=warns_embed, view=view_warns)
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
                #print(db_moderations[1])
                view_select.add_item(button_warns)
                view_select.add_item(button_bans)
                view_select.add_item(button_kicks)

                MyView.message = await ctx.send(embed=warnings_embed, view=view_select)
            else:
                await ctx.send("I see no moderations")

    @commands.command()
    async def test(self, ctx):
        button = Button(label="button-kun")

        async def button_callback(interaction):
            print("Button-kun added!")

        button.callback = button_callback

        view = MyView(timeout=10)
        view.add_item(button)
        await ctx.send(content="Testing...", view=view)

def setup(client):
    client.add_cog(Testing(client))
    print("Cog: Testing - loaded")

def teardown(client):
    print("Cog: Testing - unloaded.")
