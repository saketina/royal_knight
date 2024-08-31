import asyncio
import json

import disnake
import pyrebase
import time
from disnake.ext import commands
from disnake.ext.commands import guild_only
import datetime
from datetime import datetime as dt

import logging

logging = logging.getLogger("Utility")

firebase = pyrebase.initialize_app(
    json.load(open("./firebase_config.json", "r")))
db = firebase.database()

sniped_messages = {}
start_time = time.time()

#?# [ ] add birthday checker

class Utility(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def say(self, ctx, *, message=None):
        if message != None:
            
            if str(ctx.guild.default_role) not in message and "@here" not in message:
                msg = message
            else:
                msg = "You can\'t make me say that"
            
            
            await ctx.send(msg)
        else: 
            await ctx.send("Please tell me what to say")

    @say.before_invoke
    async def say_before(self, ctx):
        await ctx.message.delete()
    
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        sniped_messages[message.channel.id] = (message.content, message.author, message.author.display_avatar.url)

    @commands.command(
        name="snipe",
        description="Retrieve the last deleted message in this channel."
    )
    async def snipe(self, ctx):
        channel_id = ctx.channel.id
        if channel_id in sniped_messages:
            message, author, avatar_url = sniped_messages[channel_id]
            embed = disnake.Embed(title="Sniped", description=message, color=disnake.Color.dark_red())
            embed.set_author(name=author.display_name, icon_url=author.display_avatar.url)
            await ctx.send(embed=embed)
        else:
            await ctx.send(
                embed=disnake.Embed(title="Sniped", description=f"{ctx.author.mention}: There are **no deleted messages** cached on **this server**", color=disnake.Color.dark_red())
            )    
    
    @commands.command()
    async def recommend(self, ctx):
        await ctx.send("Say anything you wish to be added to the bot. It might take a while...")
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        msg = await self.client.wait_for("message", check=check)
         
        bug_channel = self.client.get_channel(1169246467182055444)
        
        embed = disnake.Embed(
            title="New recommendation!",
            description=f"From: {ctx.author}\nID: {ctx.author.id}",
            color = disnake.Color.red()
        )
        embed.add_field(
            name="Recommendation description",
            value=msg.content
        )
        await bug_channel.send(embed=embed)
        await ctx.send("Thank you for your recommendation!")

    @commands.command()
    async def bug(self, ctx):
        await ctx.send("Please tell me about the bug, i will contact the developer regarding your problem.")
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        msg = await self.client.wait_for("message", check=check)
         
        bug_channel = self.client.get_channel(965416777838391336)
        
        embed = disnake.Embed(
            title="New bug!",
            description=f"From: {ctx.author}\nID: {ctx.author.id}",
            color = disnake.Color.red()
        )
        embed.add_field(
            name="Bug description",
            value=msg.content
        )
        await bug_channel.send(embed=embed)
        await ctx.send("Thank you for your help!\nHave a nice day.")
        
    @commands.slash_command(name = "hello", description="Greets the user.")
    async def hello(self, ctx):
        await ctx.send("Hello! Pleased to meet you.")
    
    @commands.command()
    async def ping(self, ctx):
        """if round(self.client.latency * 1000) >= 200:
            color = disnake.Color.red()
        elif round(self.client.latency * 1000) >= 100:
            color = disnake.Color.yellow()
        else:
            color = disnake.Color.green()

        PingEmbed = disnake.Embed(
            title="Pong!",
            description="Current latency: "
                        f"**{round(self.client.latency * 1000)}ms**",
            color=color,
            )
        await ctx.send(embed=PingEmbed)"""
        """ Pong! """
        channel = ctx.message.channel   
        try:
            t1 = time.perf_counter()
            await ctx.trigger_typing()
            ta = t1
            t2 = time.perf_counter()
            await ctx.trigger_typing()
            tb = t2
            ra = round((tb - ta) * 1000)
        finally:
            pass
        try:
            t1a = time.perf_counter()
            await ctx.trigger_typing()
            ta1 = t1a
            t2a = time.perf_counter()
            await ctx.trigger_typing()
            tb1 = t2a
            ra1 = round((tb1 - ta1) * 1000)
        finally:
            pass
        try:
            t1b = time.perf_counter()
            await ctx.trigger_typing()
            ta2 = t1b
            t2b = time.perf_counter()
            await ctx.trigger_typing()
            tb2 = t2b
            ra2 = round((tb2 - ta2) * 1000)
        finally:
            pass
        """
        try:
            t1c = time.perf_counter()
            await ctx.trigger_typing()
            ta3 = t1c

            t2c = time.perf_counter()
            await ctx.trigger_typing()
            tb3 = t2c

            ra3 = round((tb3 - ta3) * 1000)
        finally:
            pass
        
        try:
            t1d = time.perf_counter()
            await ctx.trigger_typing()
            ta4 = t1d

            t2d = time.perf_counter()
            await ctx.trigger_typing()
            tb4 = t2d

            ra4 = round((tb4 - ta4) * 1000)
        finally:
            pass"""
            
        average_ping = round(sum([ra, ra1, ra2])/3)
            
        if round(average_ping) >= 200:
            color = disnake.Color.red()
        elif round(average_ping) >= 100:
            color = disnake.Color.yellow()
        else:
            color = disnake.Color.green()

        e = disnake.Embed(title="Pong!", colour = color)
        e.add_field(name='', value=str(ra))
        e.add_field(name='', value=str(ra1))
        e.add_field(name='', value=str(ra2))
        #e.add_field(name='', value=str(ra3))
        #e.add_field(name='', value=str(ra4))
        e.add_field(name='Average ping', value=str(round(sum([ra, ra1, ra2])/3)), inline=False)
        await ctx.send(embed=e)

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
        #?# [ ] SERVERINFO/finish command

    @commands.command(pass_context=True)
    @commands.guild_only()
    async def poll(self, ctx, *, question = None):
        if question != None:
            time=5
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

            bot_id = self.client.user.id
            #logging.info(bot_id)

            await poll_message.add_reaction(yes_mark)
            await poll_message.add_reaction(no_mark)

            await asyncio.sleep(time)

            poll_message = await ctx.channel.fetch_message(poll_message.id)
            for reaction in poll_message.reactions:
                if str(reaction.emoji) == yes_mark:
                    reactions = await reaction.users().flatten()

                    for member in reactions:
                        if member.id == bot_id:
                            pass
                        else:
                            vote_yes.append(member.display_name)

                elif str(reaction.emoji) == no_mark:
                    reactions = await reaction.users().flatten()

                    for member in reactions:
                        if member.id == bot_id:
                            pass
                        else:
                            vote_no.append(member.display_name)

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

            yes_len_count = 0
            for name in vote_yes:
                if len(in_favour) > 980:
                    in_favour += '...'
                    break
                in_favour += f'{name}\n'
                yes_len_count += len(name)

            no_len_count = 0
            for name in vote_no:
                if len(in_favour) > 980:
                    not_in_favour += '...'
                    break
                not_in_favour += f'{name}\n'
                no_len_count += len(name)

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
            finally:
                pass
        await ctx.send(f"Setting a timer for `{time}`")
        await asyncio.sleep(total_time)
        await ctx.send(f"{ctx.author.mention}, the timer is done!!!")

def setup(client):
    client.add_cog(Utility(client))

