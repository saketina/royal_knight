import asyncio
import json

import disnake
import pyrebase
from disnake.ext import commands
from disnake.ext.commands import guild_only

firebase = pyrebase.initialize_app(
    json.load(open("firebase_config.json", "r")))
db = firebase.database()


class Utility(commands.Cog):
    def __init__(self, client):
        self.client = client

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
        embed = disnake.Embed(
            title = "Server Info",
            description = f"Server Name: ``{ctx.guild.name}``",
            color = disnake.Color.dark_red()
        )
        g = await self.client.fetch_guild(ctx.guild.id)
        embed.add_field(
            name="Member Info",
            value=f"Member Count: ``{ctx.guild.member_count}``\n"
                  f"Online Members: ``{g.approximate_presence_count}``\n"
                  f"Members Boosting: ``{ctx.guild.premium_subscription_count}``\n",
            inline=False
        )
        vc_list = ctx.guild.voice_channels
        txt_list = ctx.guild.text_channels
        
        embed.add_field(
            name="Channel Info",
            value=f"Total VCs: ``{len(vc_list)}``\n"
                  f"Total Text Channels: ``{len(txt_list)}``\n",
            inline=False
        )
        created_at = ctx.guild.created_at.strftime("%d/%m/%Y")

        embed.add_field(
            name="General Info",
            value=f"Created at: ``{created_at}``\n"
                  f"Owner: ``{ctx.guild.owner}``\n"
                  f"Preferred language: ``{ctx.guild.preferred_locale}``\n"
                  f"Nitro Tier: ``{ctx.guild.premium_tier}``",
            inline=True
        )
        embed.add_field(
            name="Test",
            value="Testing"
        )
        embed.set_thumbnail(ctx.guild.icon)
        await ctx.send(embed=embed)
        # //TODO SERVERINFO/finish command

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
    
    @commands.command()
    async def timer(self, ctx, *, time: str = None):
        time_units = {"s": 1, "m": 60, "h": 3600, "d": 86400}
        total_time = 0
        
        for unit in time.split():
            try:
                value = int(unit[:-1])
                unit = unit[-1].lower()
                if unit in time_units:
                    total_time += value*time_units[unit]
                else:
                    await ctx.send("Invalid time format, use 's' for seconds, 'm' for minutes, 'h' for hours, and 'd' for days.")
                    return

            except ValueError:
                await ctx.send("Invalid time format ,use `'s'` for seconds, `'m'` for minutes, `'h'` for hours, and `'d'` for days.")
                return
        await ctx.send(f"Setting a timer for `{time}`")
        await asyncio.sleep(total_time)
        await ctx.send(f"{ctx.author.mention}, the timer is done!!!")

def setup(client):
    client.add_cog(Utility(client))
    print(f"Cog: Utility - loaded.")

def teardown(client):
    print(f"Cog: Utility - unloaded.")
