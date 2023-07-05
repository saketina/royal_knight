import disnake
from disnake.ext import commands


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(name="help", pass_context=True)
    async def help(self, ctx):
        if ctx.invoked_subcommand != None:
            return

        emb = disnake.Embed(
            title="HELP",
            description="Prefix : `k.`\nUse ``k.help [category name]`` to get more info",
            color=disnake.Color.dark_red()
        )

        emb.set_footer(
            text=f"{ctx.author.name}",
            icon_url=ctx.author.display_avatar
            )
        emb.add_field(
            name="CATEGORIES",
            value="Fun\nMisc\nModeration\nRoleplay\nUser\nUtility"
            )

        await ctx.send(embed=emb)

    @help.command(pass_context = True)
    async def test(self, ctx):
        emb = disnake.Embed(
            title = "TITLE OF CATEGORY",
            color = disnake.Color.dark_red()
            )
        emb.add_field(
            name = "TITLE OF COMMAND 1",
            value = "`COMMAND 1 USAGE`",
            inline = True
        )

        emb.add_field(
            name = "TITLE OF COMMAND 2",
            value = "`COMMAND 2 USAGE`",
            inline = False
        )
        await ctx.send(embed = emb)

    @help.command(pass_context=True)
    async def fun(self, ctx):
        emb = disnake.Embed(
            color = disnake.Color.dark_red()
            )
        emb.add_field(
            name="FUN COMMANDS",
            value="rockpaperscissors\n"
                  "`Alias: rps`"
            )
        emb.add_field(
            name="How to use",
            value="`k.rps (@user)`",
            inline=False
            )
        emb.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.display_avatar)
        await ctx.send(embed=emb)

    @help.command(pass_context=True)
    async def misc(self, ctx):
        emb = disnake.Embed(
            color = disnake.Color.dark_red()
            )
        emb.add_field(
            name="MISC COMMANDS",
            value="Status\n"
                  "Say"
            )
        emb.add_field(
            name="How to use",
            value="k.status [activity] [text]\n"
                  "k.say [message]`",
            inline=False
            )
        emb.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.display_avatar)
        await ctx.send(embed=emb)

    @help.command(pass_context=True)
    async def roleplay(self, ctx):
        emb = disnake.Embed(
            color = disnake.Color.dark_red()
            )
        emb.set_footer(
            text=f"{ctx.author.name}",
            icon_url=ctx.author.display_avatar
            )
        emb.add_field(
            name="ROLEPLAY COMMANDS",
            value="Bite\n" +
                  "Blush\n" +
                  "Bonk\n" +
                  "Boop\n" +
                  "Cry\n" +
                  "Cuddle\n" +
                  "Dance\n" +
                  "Handhold\n" +
                  "Hug\n" +
                  "Kill\n" +
                  "Kiss\n" +
                  "Nom\n" +
                  "Pat\n" +
                  "Punch\n" +
                  "Slap\n" +
                  "Smile",
            inline=False
            )
        emb.add_field(
            name="How to use",
            value="`k.[roleplay command] (@user)`",
            inline=False
            )
        await ctx.send(embed=emb)

    @help.command()
    async def moderation(self, ctx):
        emb = disnake.Embed(
            color = disnake.Color.dark_red()
            )
        emb.set_footer(
            text=f"{ctx.author.name}",
            icon_url=ctx.author.display_avatar
            )
        emb.add_field(
            name="MODERATION COMMANDS",
            value="Ban\nUnban\nKick\nWarn",
            inline=False
            )
        await ctx.send(embed=emb)

    @help.command()
    async def user(self, ctx):
        emb = disnake.Embed(
            color = disnake.Color.dark_red()
            )
        emb.set_footer(
            text=f"{ctx.author.name}",
            icon_url=ctx.author.display_avatar
            )
        emb.add_field(
            name="USER COMMANDS",
            value="Profile\n"
                  "Prefix\n"
                  "Avatar(*av*, *pfp*)",
            inline=False
            )
        emb.add_field(
            name="How to use",
            value="`k.[command] (@user)`",
            inline=False
            )
        await ctx.send(embed=emb)

    @help.command(pass_context=True)
    async def utility(self, ctx):
        emb = disnake.Embed(
            color = disnake.Color.dark_red()
            )
        emb.add_field(
            name="UTILITY COMMANDS",
            value="Afk\n"
                  "Ping\n"
                  "Pingmessages\n"
                  "Poll"
            )
        emb.add_field(
            name="How to use",
            value="`k.afk (afk message)\n"
                  "k.ping\n"
                  "k.pingmessages\n"
                  "k.poll [time] [question]`",
            inline=False
            )
        emb.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.display_avatar)
        await ctx.send(embed=emb)

def setup(client):
    client.add_cog(Help(client))
    print(f"Cog: Help - loaded.")

def teardown(client):
    print(f"Cog: Help - unloaded.")
