import disnake
import traceback
import sys
from disnake.ext import commands

class CAH(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if commands.Command.has_error_handler(self):
            return
        elif commands.Cog.has_error_handler(self):
            return
        else:
            cog = ctx.cog
            if cog:
                if cog._get_overridden_method(cog.cog_command_error) is not None:
                    return

            ignored = (commands.CommandNotFound)
            error = getattr(error, 'original', error)
            if isinstance(error, ignored):
                return
            elif isinstance(error, commands.DisabledCommand):
                await ctx.send(f"{ctx.command} has been disabled.")
            elif isinstance(error, commands.NotOwner):
                await ctx.send("You aren\'t the owner of this bot.")
            elif isinstance(error, commands.NoPrivateMessage):
                return
            else:
                # All other Errors not returned come here. And we can just print the default TraceBack.
                print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
                traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def setup(client):
    client.add_cog(CAH(client))
    print("Cog: CAH - loaded.")

def teardown(client):
    print("Cog: CAH - unloaded.")
