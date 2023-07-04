import disnake
from disnake.ext import commands, tasks
from disnake.ext.commands import guild_only, is_owner
import json

import asyncio
import aiofiles
import typing
import time
import pyrebase

firebase = pyrebase.initialize_app(
    json.load(open("firebase_config.json", "r")))
db = firebase.database()


class Utility(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.afk_dict = {}

    @commands.slash_command(name = "hello", description="Greets the user.")
    async def hello(self, ctx):
        await ctx.send("Hello! Pleased to meet you.")
    
    @commands.command(pass_context=True)
    async def ping(self, ctx):
        if round(self.client.latency * 1000) >= 155:
            color = disnake.Color.red()
        else:
            color = disnake.Color.green()

        PingEmbed = disnake.Embed(
            title="Pong!",
            description="Current latency: "
                        f"**{round(self.client.latency * 1000)}ms**",
            color=color,
            )
        await ctx.send(embed=PingEmbed)

    @commands.command()
    async def serverinfo(self, ctx):
        await ctx.send(ctx.guild.icon)

    @commands.command(pass_context=True)
    async def pingmessages(self, ctx):
        afk_mention_list = ''
        try:
            for msg_info in self.afk_dict[str(ctx.author.id) + str(ctx.guild.id)]:
                afk_mention_list += f'{msg_info}\n'

            afk_dm_embed = disnake.Embed(
                title=f'AFK mention List',
                description=afk_mention_list[:1999],
                color=disnake.Color.dark_red()
                )
            await ctx.send(embed=afk_dm_embed)

            self.afk_dict.pop(str(ctx.author.id) + str(ctx.guild.id))

        except KeyError as error:
            #print(error.__traceback__)
            await ctx.send(f'{ctx.author.mention} You had no mentions during your last afk session!')

    @commands.command(name='eval', pass_context=True)
    @commands.is_owner()
    async def eval_command(self, ctx, *, expr):
        try:
            if 'await ' in expr:
                new_expr = expr.replace('await ', '')
                ans = await eval(new_expr)
            else:
                ans = eval(expr)
            await ctx.send(f"Answer: {ans}")
        except Exception as e:
            print(e.__traceback__)
            await ctx.send("Didn't work.")

    @commands.command(pass_context=True)
    @commands.guild_only()
    async def poll(self, ctx, *, question = None):
        if question != None:
            time=20
            yes_mark="✅"
            no_mark="❎"
            poll_embed = disnake.Embed(
                title=f'Q. {question}',
                description=f"{yes_mark} YES \n"
                            f"{no_mark} NO",
                color=disnake.Color.dark_red()
                )
            poll_embed.set_author(
                name=ctx.author.display_name,
                icon_url=ctx.author.display_avatar
                )
            poll_message = await ctx.send(embed=poll_embed)
            vote_yes = []
            vote_no = []
            vote = {'yes': [], 'no': []}
            bot = await self.client.fetch_user(850019720648589352)
            bot_name = bot.display_name

            await poll_message.add_reaction(yes_mark)
            await poll_message.add_reaction(no_mark)

            await asyncio.sleep(time)

            poll_message = await ctx.channel.fetch_message(poll_message.id)
            for reaction in poll_message.reactions:

                if str(reaction.emoji) == yes_mark:
                    reactions = await reaction.users().flatten()

                    for member in reactions:
                        vote_yes.append(member.display_name)
                        yx = slice(0, 1)

                elif str(reaction.emoji) == no_mark:
                    reactions = await reaction.users().flatten()

                    for member in reactions:
                        vote_no.append(member.display_name)
                        nx = slice(0, 1)

            vote_yes[yx] = ""
            vote_no[nx] = ""

            if vote_yes<vote_no:
                poll_answer = "Majority is in opposition of the poll"
                color=disnake.Color.red()
            elif vote_yes>vote_no:
                poll_answer = "Majority is in favour of the poll"
                color=disnake.Color.green()
            elif len(vote_yes) == 0 and  len(vote_no) == 0:
                poll_answer = "Nobody voted..."
                color=disnake.Color.gold()
            else:
                poll_answer = "It was a tie!"
                color = disnake.Color.gold()

            result_embed = disnake.Embed(
                title=f'Poll: {question}',
                description=f"**Results:**\n{poll_answer}\n"
                            f'\n**Link:** {poll_message.jump_url}',
                color=color
                )
            result_embed.set_author(
                name=ctx.author.display_name,
                icon_url=ctx.author.display_avatar
                )

            in_favour = 'Nobody' if len(vote_yes) == 0 else ''
            not_in_favour = 'Nobody' if len(vote_no) == 0 else ''

            len_count = 0
            for name in vote_yes:
                if len(in_favour) > 980:
                    in_favour += '...'
                    break
                in_favour += f'{name}\n'
                len_count += len(name)

            len_count = 0
            for name in vote_no:
                if len(in_favour) > 980:
                    not_in_favour += '...'
                    break
                not_in_favour += f'{name}\n'
                len_count += len(name)

            result_embed.add_field(
                name=f'People in Favour: {len(vote_yes)}',
                value=in_favour
                )
            result_embed.add_field(
                name=f'People not in Favour: {len(vote_no)}',
                value=not_in_favour
                )

            await ctx.send(embed=result_embed)
        else:
            embed = disnake.Embed(
                title = "POLL HELP",
                description="`k.poll [question]`",
                color=disnake.Color.dark_red()
                )
            await ctx.send(embed=embed)

    @commands.command(name="toggle", pass_context=True)
    @commands.is_owner()
    async def toggle(self, ctx, *, command):
        command = self.client.get_command(command)

        if command is None:
            embed = disnake.Embed(title="ERROR", description="I can't find a command with that name!", color=0xff0000)
            await ctx.send(embed=embed)

        elif ctx.command == command:
            embed = disnake.Embed(title="ERROR", description="You cannot disable this command.", color=0xff0000)
            await ctx.send(embed=embed)

        else:
            command.enabled = not command.enabled
            ternary = "enabled" if command.enabled else "disabled"
            embed = disnake.Embed(title="Toggle", description=f"I have {ternary} {command.qualified_name} for you!", color=0xff00c8)
            await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def leave(self, ctx, *, guildinput):
        try:
            guildid = int(guildinput)
        except:
            await ctx.send("Invalid guild: failed to convert to int")

        try:
            guild = self.client.get_guild(guildid)
        except:
            await ctx.send("Invalid guild")

        try:
            await guild.leave()
            await ctx.send(f"left {guild.name}")
        except:
            await ctx.send("Error leaving")

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def servers(self, ctx):
        await ctx.send(f"{len(self.client.guilds)}")
        listofids = []
        for guild in self.client.guilds:
            listofids.append(guild.id)
        await ctx.send(listofids)

def setup(client):
    client.add_cog(Utility(client))
    print(f"Cog: Utility - loaded.")

def teardown(client):
    print(f"Cog: Utility - unloaded.")
