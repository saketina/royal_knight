# TODO finish global error handler
# TODO transfer error handlers to GAH
# TODO add MISSING PERMISSIONS handler for muted cmd(happens when user tries to unmute themselves + they arent muted)
import sys
import traceback

import disnake
from disnake.ext import commands


class CommandErrorHandler(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        Parameters
        ------------
        ctx: commands.Context
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        # This prevents any cogs with an overwritten cog_command_error being handled here.
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound)

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return

        if isinstance(error, commands.CommandInvokeError):
            #print("should not be here")
            if ctx.command.qualified_name == "unban":
                await ctx.send(content = "I can\'t find that member.", delete_after = 10)
            else:
                await ctx.send("I didn\'t quite catch that.")

        elif isinstance(error, commands.BotMissingPermissions):
            if ctx.command.qualified_name == "unban":
                await ctx.send(BotMissingPermissions.missing_permissions)
            elif ctx.command.qualified_name == "kick":
                await ctx.send(BotMissingPermissions.missing_permissions)

        elif isinstance(error, commands.CheckFailure):
            return
        
        # For this error handler we check if the user has truly set a role in args
        elif isinstance(error, commands.RoleNotFound):
            await ctx.send(error)
        
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(error)
        
        elif isinstance(error, commands.UserNotFound):
            await ctx.send(error)

        # For this error handler we check if the command has been disabled
        elif isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.command} has been disabled.')

        # For this error handler we check if someone has DMs off
        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except disnake.HTTPException:
                pass

        elif isinstance(error, commands.MissingPermissions):
            try:
                await ctx.send(f"I\'m missing permissions for this!\nPermissions missing:{commands.MissingPermissions(missing_permissions=error.missing_permissions)}")
            except:
                await ctx.author.send(f"I\'m missing permissions for this!\nPermissions missing:{commands.missing_permissions}")
        elif isinstance(error, commands.MemberNotFound):
            if ctx.command.qualified_name == "ban":
                await ctx.send(content = "I couldn\'t find that person", delete_after = 10)
        
        elif isinstance(error, commands.UserNotFound):
            if ctx.command.qualified_name == "ban":
                await ctx.send(content = "I couldn\'t find that person", delete_after = 10)

        # For this error example we check to see where it came from...
        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == "purge":
                await ctx.send(content = "Please input only numbers.", delete_after = 10)
            elif ctx.command.qualified_name == "unban":
                await ctx.send(content = "Please input only the members id.", delete_after = 10)

        elif isinstance(error, disnake.Forbidden):
            #print("should be here")
            #print(error.code)
            if error.code == 50013:
                #print("done goofeds")
                await ctx.author.send("I seem to be missing permissions to speak in that channel, please contact an administrator")
                return

        else:
            # All other Errors not returned come here. And we can just print the default TraceBack.
            print('Ignoring exception in command {}:'.format(ctx.command), error, file=sys.stderr)
            #traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def setup(client):
    client.add_cog(CommandErrorHandler(client))
    print(f"Cog: GAH - loaded.")

def teardown(client):
    print(f"Cog: GAH - unloaded.")