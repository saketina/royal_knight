import disnake
import random

from disnake.ext import commands
from disnake.ui import Button
import datetime
from datetime import datetime as dt

import logging

logging = logging.getLogger("Rps")

def author_check(ctx, interaction):
    if interaction.author.id == ctx.author.id:
        return True
    else:
        return False
    
def build_outcome(players, answers, winner):
    finalOptions = {
                "1": "Rock",
                "2": "Paper",
                "3": "Scissors"
                }
    if winner == "Draw":
        ecolor = disnake.Color.yellow()
    elif winner == f"{players[0]} won":
        ecolor = disnake.Color.green()
    elif winner == f"{players[1]} won":
        ecolor = disnake.Color.red()
    embed = disnake.Embed(
        title=f"{players[0]} VS {players[1]}",
        timestamp=dt.now(),
        color=ecolor
    )
    embed.add_field(
        name=f"Outcome: {winner}",
        value=f"{players[0]}: {finalOptions[answers[0]]}\n"
                f"{players[1]}: {finalOptions[answers[1]]}"
    )
    return embed

class MyView(disnake.ui.View):
    def __init__(self, timeout: float, interaction:disnake.Interaction):
        super().__init__(timeout=timeout)

    async def on_timeout(self):
        try:
            if self.message != None:  # type: ignore
                await self.message.edit(view=None) # type: ignore
        except:
            interaction = self.interaction  # type: ignore
            await interaction.edit_original_message(view=None)
            
class MyView2(disnake.ui.View):
    def __init__(self, timeout: float, interaction:disnake.Interaction):
        super().__init__(timeout=timeout)

    async def on_timeout(self):
        try:
            if self.message != None:  # type: ignore
                await self.message.edit(view=None) # type: ignore
        except:
            interaction = self.interaction  # type: ignore
            await interaction.edit_original_message(view=None)

class rps(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.player2_answer = 0
        
    @commands.command()
    async def join(self, ctx):
        await ctx.send("1"+"1")
    
    @commands.command(aliases=["rps"])
    @commands.guild_only()
    async def rockpaperscissors(self, ctx, target: disnake.Member = None):
        player1 = ctx.author
        if target == ctx.author or target == None:
            player2 = "CPU"
        else:
            player2 = target
            
        cpu_options = "1", "2", "3"
        
        
        options = {
            "11": 0,
            "12": 2,
            "13": 1,
            "21": 1,
            "22": 0,
            "23": 2,
            "31": 2,
            "32": 1,
            "33": 0,
        }
        
        start_embed = disnake.Embed(
            title="Rock Paper Scissors",
            description="Choose one of the following: \n"
                        "1. Rock\n"
                        "2. Paper\n"
                        "3. Scissors",
            color=disnake.Color.dark_red()
        )
        start_embed.set_footer(text=f"{player1} VS {player2}")
        
        button_rock1 = Button(label="Rock")
        button_paper1 = Button(label="Paper")
        button_scissors1 = Button(label="Scissors")
        
        button_rock2 = Button(label="Rock")
        button_paper2 = Button(label="Paper")
        button_scissors2 = Button(label="Scissors")
        
        async def button_rock_callback2(interaction):
            self.player2_answer = "1"
            await interaction.response.edit_message(view=None)

        async def button_paper_callback2(interaction):
            return "2"
        async def button_scissors_callback2(interaction):
            return "3"
        
        button_rock2.callback = button_rock_callback2
        button_paper2.callback = button_paper_callback2
        button_scissors2.callback = button_scissors_callback2
        
        view_select2 = MyView2(timeout=30, interaction=[button_rock_callback2, button_paper_callback2, button_scissors_callback2])
        view_select2.add_item(button_rock2)
        view_select2.add_item(button_paper2)
        view_select2.add_item(button_scissors2)
        
        player1_answer = 0
        async def button_rock_callback1(interaction):
            if author_check(ctx, interaction):
                #await interaction.response.edit_message(content="rock", embed=None, view=None)
                player1_answer = "1"
                
                if player1_answer != 0:
                    if player2 == "CPU":
                        player2_answer = random.choice(cpu_options)
                    else:
                        MyView2.message = await player2.send(embed=start_embed, view=view_select2)
                        await self.client.wait_for(
                        "button_click",
                        check=lambda i: i.author.id==player2.id and i.channel==player2.dm_channel,
                        timeout=30
                        )
                        print(self.player2_answer)
                
                get_outcome = player1_answer+"1"
                outcome = options[get_outcome]
                
                if outcome == 0:
                    winner = "Draw"
                elif outcome == 1:
                    winner = f"{player1} won"
                elif outcome == 2:
                    winner = f"{player2} won"
                
                await interaction.response.edit_message(embed=build_outcome(players=[player1, player2], answers=[player1_answer, "1"], winner=winner), view=None)
            
            else:
                return
            
        async def button_paper_callback1(interaction):
            if author_check(ctx, interaction):
                #await interaction.response.edit_message(content="paper", embed=None, view=None)
                player1_answer = "2"
            
            else:
                return
            
        async def button_scissors_callback1(interaction):
            if author_check(ctx, interaction):
                #await interaction.response.edit_message(content="scissors", embed=None, view=None)
                player1_answer = "3"
            
            else:
                return
            
                    
        button_rock1.callback = button_rock_callback1           
        button_paper1.callback = button_paper_callback1
        button_scissors1.callback = button_scissors_callback1
        
        view_select1 = MyView(timeout=30, interaction=[button_rock_callback1, button_paper_callback1, button_scissors_callback1])
        
        view_select1.add_item(button_rock1)
        view_select1.add_item(button_paper1)
        view_select1.add_item(button_scissors1)
        
        MyView.message = await ctx.send(embed=start_embed, view=view_select1)
        async def on_error(self, error, item, interaction):
            print(error)
        
def setup(client):
    client.add_cog(rps(client))
