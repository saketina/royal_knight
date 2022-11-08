import disnake, datetime
from disnake.ext import commands
from datetime import datetime

class Sinner(commands.Converter):
    async def convert(self, ctx, argument):
        argument = await commands.MemberConverter().convert(ctx, argument) # gets a member object
        permission = argument.guild_permissions.manage_messages # can change into any permission
        if not permission: # checks if user has the permission
            return argument # returns user object
        else:
            raise commands.BadArgument("You cannot punish other staff members") # tells user that target is a staff member

class Redeemed(commands.Converter):
    async def convert(self, ctx, argument):
        argument = await commands.MemberConverter().convert(ctx, argument) # gets member object
        muted = disnake.utils.get(ctx.guild.roles, name="Muted") # gets role object
        if muted in argument.roles: # checks if user has muted role
            return argument # returns member object if there is muted role
        else:
            raise commands.BadArgument("The user was not muted.") # self-explainatory

class Moderation(commands.Cog, description="A group of commands that are used for moderating"):
    def __init__(self, client):
        self.client = client

    async def __error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(error)

    @commands.command(name="ban", help="!ban [@mention/member id] {reason}")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user:Sinner = None, *, reason=None):
        if not user: # checks if there is a user
            return await ctx.send("You must specify a user")

        if user is str:
            user = await self.client.fetch_user(int(user))
        else:
            pass

        try: # Tries to ban user
            guild = ctx.guild
            await guild.ban(
            user,
            reason=f"By {ctx.author} for {reason}"
            )
            await ctx.send(f"{user.mention} was banned for {reason}.")
        except disnake.Forbidden:
            return await ctx.send("Are you trying to ban someone higher than the bot?")

    @commands.command()
    #@guild_only()  # Might not need ()
    async def unban(self, ctx, id: int):
        user = await self.client.fetch_user(id)
        await ctx.guild.unban(user)
        await ctx.send(f"{user.display_name} has been unbanned.")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: Sinner=None, reason=None):
        if not user:
            return await ctx.send("You must specify a user")

        try:
            await ctx.guild.kick(user, f"By {ctx.author} for {reason}" or f"By {ctx.author} for None Specified")
        except discord.Forbidden:
            return await ctx.send("Are you trying to kick someone higher than the bot?")

    @commands.command()
    @commands.has_permissions(delete_messaages=True)
    async def purge(self, ctx, limit: int):
        await ctx.purge(limit=limit + 1)
        await ctx.send(f"Bulk deleted `{limit}` messages")

    @commands.command()
    async def unmute(self, ctx, user: Redeemed):
        await user.remove_roles(disnake.utild.get(ctx.guild.roles, name="Muted"))
        await ctx.send(f"{user.mention} has been unmuted")


    @commands.command()
    async def mute(self, ctx, user: Sinner, reason=None):
        if not user:
            return await ctx.send("You must specify a user")

        await mute(ctx, user, reason)

def setup(client):
    client.add_cog(Moderation(client))
