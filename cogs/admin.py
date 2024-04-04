import disnake
from disnake.ext import commands
from disnake.ext.commands import has_permissions


class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="toggle", pass_context=True)
    @commands.has_permissions(administrator=True)
    async def toggle(self, ctx, *, command=None):
        if command==None:
            await ctx.send("Please tell me which command to toggle.")
            return
        else:
            pass

        command = self.client.get_command(command)

        if command is None:
            embed = disnake.Embed(title="ERROR", description="I can't find a command with that name!", color=disnake.Color.brand_red())
            await ctx.send(embed=embed)

        elif ctx.command == command:
            embed = disnake.Embed(title="ERROR", description="You cannot disable this command.", color=disnake.Color.brand_red())
            await ctx.send(embed=embed)

        else:
            command.enabled = not command.enabled
            ternary = "enabled" if command.enabled else "disabled"
            color = disnake.Color.green() if command.enabled else disnake.Color.dark_red()
            embed = disnake.Embed(title="Toggle", description=f"I have {ternary} {command.qualified_name} for you!", color=color)
            await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def load(self, ctx, input=None):
        cog = input.lower()
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
            self.client.load_extension(f"cogs.{cog}")
            await ctx.send(f"Cog: **{cog}** has been loaded!")

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def unload(self, ctx, input=None):
        cog = input.lower()
        if cog != None:
            self.client.unload_extension(f"cogs.{cog}")
            await ctx.send(f"Cog: **{cog}** has been unloaded!")
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
    async def reload(self, ctx, input=None):
        cog = input.lower()
        if cog != None:
            self.client.reload_extension(f"cogs.{cog}")
            await ctx.send(f"Cog: **{cog}** has been reloaded!")
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