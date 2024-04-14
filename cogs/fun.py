import asyncio
import random
import typing

import disnake
from disnake import Forbidden
from disnake.ext import commands

import logging

logging = logging.getLogger("Fun")

# TODO RPS/remove error handler and add try/except
# ! BUG tested the int vs int values
# ! need to test str vs str, str vs int, int vs str
# ! need to test the same with user vs CPU


class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.max_concurrency(1, per=commands.BucketType.user)
    @commands.command(aliases=['rps'], pass_context=True)
    async def rockpaperscissors(self, ctx, player: disnake.Member = None):
        if player != ctx.author:
            rejected = False
            options = [
                'Rock',
                'Paper',
                'Scissors'
                ]
            finalOptions = {
                "1": "Rock",
                "2": "Paper",
                "3": "Scissors"
                }
            answer = False

            def process_input(selection: typing.Union[int, str]):
                if type(selection) == str:
                    return selection

                elif type(selection) == int:
                    return options[selection-1]

            answer_options = {
                'RockRock': 0,
                'RockPaper': 2,
                'RockScissors': 1,
                'PaperRock': 1,
                'PaperPaper': 0,
                'PaperScissors': 2,
                'ScissorsRock': 2,
                'ScissorsPaper': 1,
                'ScissorsScissors': 0,
                '1Rock': 0,
                '1Paper': 2,
                '1Scissors': 1,
                '2Rock': 1,
                '2Paper': 0,
                '2Scissors': 2,
                '3Rock': 2,
                '3Paper': 1,
                '3Scissors': 0,
                '11': 0,
                '12': 2,
                '13': 1,
                '21': 1,
                '22': 0,
                '23': 2,
                '31': 2,
                '32': 1,
                '33': 0,
                'Rock1': 0,
                'Rock2': 2,
                'Rock3': 1,
                'Paper1': 1,
                'Paper2': 0,
                'Paper3': 2,
                'Scissors1': 2,
                'Scissors2': 1,
                'Scissors3': 0
                }

            bot_answer = random.choice(options)
            rps_embed = disnake.Embed(
                title='Rock Paper Scissors',
                description='Choose one of the following: \n'
                            '1. Rock\n'
                            '2. Paper\n'
                            '3. Scissors\n',
                color=disnake.Color.dark_red()
                )

            win_embed = disnake.Embed(
                title="You won!",
                description=f'{ctx.author.display_name} Vs CPU\n'
                            f'I chose ``{bot_answer}``\n',
                color=disnake.Color.green()
                )

            lose_embed = disnake.Embed(
                title="You lost...",
                description=f'{ctx.author.display_name} Vs CPU\n'
                            f'I chose ``{bot_answer}``\n',
                color=disnake.Color.red()
                )
            try:
                if player is None:
                    await ctx.send(
                        f'{ctx.author.mention} Choose: ',
                        embed=rps_embed
                        )
                    reply = await self.client.wait_for(
                        "message",
                        check=lambda m: m.author.id==ctx.author.id and m.channel==ctx.channel,
                        timeout=30
                        )
                else:
                    await ctx.author.send(
                        f'{ctx.author.mention} Choose: ',
                        embed=rps_embed
                        )
                    reply = await self.client.wait_for(
                        "message",
                        check=lambda m: m.author.id==ctx.author.id and m.channel==ctx.author.dm_channel,
                        timeout=30
                        )

                answer = process_input(reply.content).lower().capitalize()
            except Forbidden:
                    await ctx.send("You have your DMs off I can\'t send you a message")
            except asyncio.TimeoutError:
                if player is None:
                    await ctx.send(
                        f'{ctx.author.mention} You took too much time to reply. I am not playing with you'
                        )
                else:
                    await ctx.send(
                        f'{ctx.author.mention} You wasted too much time. Don\'t run the command if you don\'t want to play.'
                        )

            if player is not None:
                try:
                    await player.send(
                        f'{player.mention}!\n{ctx.author.display_name} has challenged you to a Rock Paper Scissors '
                        'match. Send your answer here to Accept challenge or ignore to decline.\n'
                        'You have to answer in 30 seconds',
                        embed=rps_embed
                        )
                    mp_reply = await self.client.wait_for(
                        "message",
                        check=lambda m: m.author.id==player.id and m.channel==player.dm_channel,
                        timeout=30
                        )
                    mp_answer = process_input(mp_reply.content).lower().capitalize()

                except Forbidden:
                    await ctx.send(f'{ctx.author.mention} {player.display_name} have their DMs closed or have blocked'
                        ' me *cries*. You can\'t play with them.'
                        )

                except asyncio.TimeoutError:
                    await ctx.send(f'{ctx.author.mention} {player.display_name} doesn\'t want to play with you. So I\'ll'
                                ' play with you so you don\'t feel rejected.'
                                )
                    mp_answer = bot_answer
                    rejected = True
                
                # ! BUG HERE SOMEWHERE RPS FUCKED
                if answer_options[answer+mp_answer] == 0:
                    if answer.isnumeric():
                        final_options = finalOptions.get(answer)
                    else:
                        final_options = answer

                    if mp_answer.isnumeric():
                        mp_final_options = finalOptions.get(mp_answer)
                    else:
                        mp_final_options = mp_answer

                    tie_emb_auth = disnake.Embed(
                        description="F. That was a tie",
                        color= disnake.Color.gold()
                        )
                    tie_emb_auth.add_field(
                        name = "Answers",
                        value = f"Your answer: `{final_options}`\nOpponent\'s answer: ``{mp_final_options}`"
                        )

                    tie_emb = disnake.Embed(
                        description="F. That was a tie",
                        color= disnake.Color.gold()
                        )
                    tie_emb.add_field(
                        name = "Answers",
                        value = f"Your answer: `{mp_final_options}`\nOpponent\'s answer: ``{final_options}``"
                        )

                    await ctx.author.send(
                        embed=tie_emb_auth
                        )
                    await player.send(
                        embed=tie_emb
                        )

                elif answer_options[answer+mp_answer] == 1:
                    if rejected:
                        won_emb = disnake.Embed(
                            title="You won!",
                            description=f'{ctx.author.display_name} Vs CPU\n'
                                        f'I chose ``{bot_answer}``\n',
                            color=disnake.Color.green()
                            )

                        await ctx.send(
                            embed=won_emb
                            )
                    else:
                        if answer.isnumeric():
                            final_options = finalOptions.get(answer)
                        else:
                            final_options = answer

                        if mp_answer.isnumeric():
                            mp_final_options = finalOptions.get(mp_answer)
                        else:
                            mp_final_options = mp_answer

                        DMwin_embed = disnake.Embed(
                            title="You won!",
                            color=disnake.Color.green()
                            )
                        DMwin_embed.add_field(
                            name = f'{ctx.author.display_name} Vs {player.display_name}',
                            value = f'Your answer: ``{final_options}``\n'
                                    f'The opponent\'s answer: ``{mp_final_options}``\n'
                            )

                        DMlose_embed = disnake.Embed(
                            title="You lost...",
                            color=disnake.Color.red()
                            )
                        DMlose_embed.add_field(
                            name = f'{player.display_name} Vs {ctx.author.display_name}',
                            value = f'Your answer: ``{mp_final_options}``\n'
                                    f'The opponent\'s answer: ``{final_options}``\n'
                            )

                        await ctx.author.send(
                            f'{ctx.author.mention}',
                            embed=DMwin_embed
                            )
                        await player.send(
                            f'{player.mention}',
                            embed=DMlose_embed
                            )

                elif answer_options[answer+mp_answer] == 2:
                    if rejected:

                        lost_emb = disnake.Embed(
                            title="You lost...",
                            description=f'{ctx.author.display_name} Vs CPU\n'
                                        f'I chose ``{bot_answer}``\n'
                                        'Looks like I won. Git gud m8.',
                            color=disnake.Color.red()
                            )

                        await ctx.send(
                            embed=lost_emb
                            )
                    else:
                        if answer.isnumeric():
                            final_options = finalOptions.get(answer)
                        else:
                            final_options = answer

                        if mp_answer.isnumeric():
                            mp_final_options = finalOptions.get(mp_answer)
                        else:
                            mp_final_options = mp_answer

                        DMwin_embed = disnake.Embed(
                            title="You won!",
                            color=disnake.Color.green()
                            )
                        DMwin_embed.add_field(
                            name = f'{ctx.author.display_name} Vs {player.display_name}',
                            value = f'Your answer: ``{mp_final_options}``\n'
                                    f'The opponent\'s answer: ``{final_options}``\n'
                            )

                        DMlose_embed = disnake.Embed(
                            title="You lost...",
                            color=disnake.Color.red()
                            )
                        DMlose_embed.add_field(
                            name = f'{player.display_name} Vs {ctx.author.display_name}',
                            value = f'Your answer: ``{final_options}``\n'
                                    f'The opponent\'s answer: ``{mp_final_options}``\n'
                            )

                        await ctx.author.send(
                            f'{ctx.author.mention}',
                            embed=DMlose_embed
                            )
                        await player.send(
                            f'{player.mention}',
                            embed=DMwin_embed
                            )

            else:
                if answer_options[answer+bot_answer] == 0:

                    tie_emb = disnake.Embed(
                        description="F. That was a tie",
                        color= disnake.Color.gold()
                        )
                    await ctx.send(
                        embed=tie_emb
                        )

                elif answer_options[answer+bot_answer] == 1:

                    won_emb = disnake.Embed(title="You won!",
                        description=f'{ctx.author.display_name} Vs CPU\n'
                                    f'I chose ``{bot_answer}``\n',
                        color=disnake.Color.green()
                        )
                    await ctx.send(
                        embed=won_emb
                        )

                elif answer_options[answer+bot_answer] == 2:

                    lost_emb = disnake.Embed(
                        title="You lost...",
                        description=f'{ctx.author.display_name} Vs CPU\n'
                                    f'I chose ``{bot_answer}``\n',
                        color=disnake.Color.red()
                        )
                    await ctx.send(
                        embed=lost_emb
                        )
        else:
            await ctx.send("You can\'t start a match with yourself")
    """
    @rockpaperscissors.error
    async def rps_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send("Thats an invalid answer, please start a new round.")
    """
def setup(client):
    client.add_cog(Fun(client))
    print(f"Cog: Fun - loaded.")

def teardown(client):
    print(f"Cog: Fun - unloaded.")