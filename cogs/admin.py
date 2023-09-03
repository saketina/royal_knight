import disnake
from disnake.ext import commands
from disnake.ext.commands import has_permissions


class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def load(self, ctx, cog=None):
        if cog == None:
            emb = disnake.Embed(
                title="Load command help",
                description="Loads a command category.\nEnabling all the commands in that category.",
                color=disnake.Color.dark_red()
            )
            emb.add_field(
                name="Usage",
                value="```k.load <category_name>```"
            )
            await ctx.send(embed=emb)
        else:
            try:
                self.client.load_extension(f"cogs.{cog}")
                await ctx.send(f"Cog: **{cog}** has been loaded!")
            except commands.ExtensionAlreadyLoaded:
                await ctx.send(f"Error: **{cog}** is already loaded.")
            except commands.ExtensionNotFound:
                await ctx.send(f"I could not find **{cog}**")
            except Exception as e:
                print(f"Error: \nType: {type(e).__name__} \nInfo - {e}")

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def unload(self, ctx, cog=None):
        if cog != None:
            try:
                self.client.unload_extension(f"cogs.{cog}")
                await ctx.send(f"Cog: **{cog}** has been unloaded!")
            except commands.ExtensionNotLoaded:
                await ctx.send(f"Error: **{cog}** is not loaded.")
            except commands.ExtensionNotFound:
                await ctx.send(f"I could not find **{cog}**")
            except Exception as e:
                print(f"Error: \nType: {type(e).__name__} \nInfo - {e}")
        else:
            emb = disnake.Embed(
                title="Unload command help",
                description="Unloads a command category.\nMaking all the commands in that category disabled.",
                color=disnake.Color.dark_red()
            )
            emb.add_field(
                name="Usage",
                value="```k.unload <category_name>```"
            )
            await ctx.send(embed=emb)


    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def reload(self, ctx, cog=None):
        if cog != None:
            try:
                self.client.reload_extension(f"cogs.{cog}")
                await ctx.send(f"Cog: **{cog}** has been reloaded!")
            except commands.ExtensionNotLoaded:
                await ctx.send(f"Error: **{cog}** is not loaded.")
            except commands.ExtensionNotFound:
                await ctx.send(f"I could not find **{cog}**")
            except Exception as e:
                print(f"Error: \nType: {type(e).__name__} \nInfo - {e}")
        else:
            emb = disnake.Embed(
                title="Reload command help",
                description="Reloads a command category in case of an error.\nIf the error persists please contact the dev.",
                color=disnake.Color.dark_red()
            )
            emb.add_field(
                name="Usage",
                value="```k.reload <category_name>```"
            )
            await ctx.send(embed=emb)


def setup(client):
    client.add_cog(Admin(client))
    print(f"Cog: Admin - loaded.")

def teardown(client):
    print(f"Cog: Admin - unloaded.")