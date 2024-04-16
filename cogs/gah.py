
# TODO add MISSING PERMISSIONS handler for muted cmd(happens when user tries to unmute themselves + they arent muted)
import sys
import traceback

import disnake
from disnake.ext import commands

import logging

logging = logging.getLogger("GAH")

class CommandErrorHandler(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

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
            if ctx.command.qualified_name == "unban":
                await ctx.send(content = "I can\'t find that member.", delete_after = 10)
            elif ctx.command.qualified_name == "prefix":
                await ctx.send("I can't find that in the list.")
            else:
                pass
        
        elif isinstance(error, commands.ExtensionNotFound):
            await ctx.send(f"I could not find **{ctx.args[-1]}**")
        
        elif isinstance(error, commands.ExtensionAlreadyLoaded):
            await ctx.send(f"Error: **{ctx.args[-1]}** is already loaded.")
        
        elif isinstance(error, commands.ExtensionNotLoaded):
            await ctx.send(f"Error: **{ctx.args[-1]}** is not loaded.")

        elif isinstance(error, commands.BotMissingPermissions):
            try:
                await ctx.send(error)
            except disnake.Forbidden as f:
                if f.code == 50013:
                    await ctx.author.send("I seem to be missing permissions to speak in that channel, please contact an administrator")
                    return
                else:
                    pass

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
            
        elif isinstance(error, commands.NotOwner):
            return
        
        elif isinstance(error, AttributeError):
            if ctx.command.qualified_name == "ban":
                await ctx.send("User not found.")
            else:
                pass

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You seem to be missing permissions")
            
        # For this error example we check to see where it came from...
        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == "purge":
                await ctx.send(content = "Please input only numbers.", delete_after = 10)
            elif ctx.command.qualified_name == "unban":
                await ctx.send(content = "Please input only the members id.", delete_after = 10)

        elif isinstance(error, disnake.Forbidden):
            if ctx.command.qualified_name == "ban":
                await ctx.send("You can\'t ban that user.")
            elif ctx.command.qualified_name == "kick":
                await ctx.send("You can\'t ban that user.")            
            else:
                pass

        else:
            # All other Errors not returned come here. And we can just print the default TraceBack.
            logging.error('Ignoring exception in command {}:'.format(ctx.command), error, file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            embed = disnake.Embed(
                title=f"Error in command {ctx.command.qualified_name}",
                description=error,
                color=disnake.Color.red()
            )
            await ctx.send("Please send this to the developer.", embed=embed)

def setup(client):
    client.add_cog(CommandErrorHandler(client))
