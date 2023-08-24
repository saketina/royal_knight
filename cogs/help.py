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
            value="```Fun\nModeration\nRoleplay\nUser\nUtility\nMisc```"
            )

        await ctx.send(embed=emb)

    @help.command(pass_context=True)
    async def fun(self, ctx):
        emb = disnake.Embed(
            title = "FUN COMMANDS",
            color = disnake.Color.dark_red()
            )
        emb.add_field(
            name="Rock Paper Scissors\n"
                  "`Alias: rps`",
            value="```k.rps (@user)```"
            )
        emb.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.display_avatar)
        await ctx.send(embed=emb)

    @help.command(pass_context=True)
    async def misc(self, ctx):
        emb = disnake.Embed(
            title = "MISC COMMANDS",
            color = disnake.Color.dark_red()
            )
        emb.add_field(
            name="Status",
            value="```k.status [activity] [text]```"
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
            title = "MODERATION COMMANDS",
            color = disnake.Color.dark_red()
            )
        emb.add_field(
            name="Purge",
            value="```k.purge [amount]```",
            inline=False
            )
        emb.add_field(
            name="Warn",
            value="```k.warn [member_id/@member] [reason]```",
            inline=False
            )
        emb.add_field(
            name="Kick",
            value="```k.kick [mention/user_id] (reason)```",
            inline=False
            )
        emb.add_field(
            name="Ban",
            value="```k.ban [mention/user_id] (reason)```",
            inline=False
            )
        emb.add_field(
            name="Unban",
            value="```k.unban [user_id]```",
            inline=False
            )
        emb.set_footer(
            text=f"{ctx.author.name}",
            icon_url=ctx.author.display_avatar
            )
        await ctx.send(embed=emb)

    @help.command()
    async def user(self, ctx):
        emb = disnake.Embed(
            title="USER COMMANDS",
            color = disnake.Color.dark_red()
            )
        emb.add_field(
            name="Profile",
            value="```k.[profile] (@user)```",
            inline=False
            )
        emb.add_field(
            name="Prefix",
            value="```k.[prefix] (add/remove)```",
            inline=False
            )
        emb.add_field(
            name="Avatar\n`alias:av, pfp`",
            value="```k.[avatar] (@user)```",
            inline=False
            )
        emb.set_footer(
            text=f"{ctx.author.name}",
            icon_url=ctx.author.display_avatar
            )
        await ctx.send(embed=emb)

    @help.command(pass_context=True)
    async def utility(self, ctx):
        emb = disnake.Embed(
            title="UTILITY COMMANDS",
            color = disnake.Color.dark_red()
            )
        emb.add_field(
            name="Ping",
            value="```k.ping```",
            inline=False
            )
        emb.add_field(
            name="Pingmessages",
            value="```k.pingmessages```",
            inline=False
            )
        emb.add_field(
            name="Poll",
            value="```k.poll [time] [question]```",
            inline=False
            )
        emb.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.display_avatar)
        await ctx.send(embed=emb)

def setup(client):
    client.add_cog(Help(client))
    print(f"Cog: Help - loaded.")

def teardown(client):
    print(f"Cog: Help - unloaded.")
