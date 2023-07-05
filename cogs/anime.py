import random

import disnake
from disnake.ext import commands

# //TODO remove unneeded imports and lines of code

def opening_check(msg):
    allowed_users = [
        457948769216888833,    # Ansh
        503452026391494676,    # Zeus
        378828816501702667,    # Arcane
        466692642856763392,    # Dracule
        385683162799538176,    # Deni
        ]
    if msg.author.id in allowed_users:
        return True
    else:
        return False


class Anime(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.openings_list = []

        with open('cogs/Assets/openings.txt', encoding='utf-8') as file:
            self.openings_list = file.readlines()

    @commands.command(aliases=['getops', 'getopenings', 'get_opening'])
    @commands.check(opening_check)
    async def get_openings(self, ctx, number_of_op: int = 10):
        op_len = len(self.openings_list)
        return_list = set()

        while len(return_list) < number_of_op:
            index = random.randint(0, op_len - 1)
            return_list.add(self.openings_list[index])

        return_msg = ''
        count = 1

        for op in return_list:
            return_msg += str(count) + '. ' + op
            count += 1

        openings_embed = disnake.Embed(
            title=f'List of {number_of_op} Random Openings',
            description=return_msg,
            color=disnake.Color.dark_red()
            )
        await ctx.send(embed=openings_embed)

def setup(client):
    client.add_cog(Anime(client))
    print(f"Cog: Anime - loaded.")

def teardown(client):
    print(f"Cog: Anime - unloaded.")
