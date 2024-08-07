import json
import os
import platform

import disnake
import psutil
import pyrebase
from disnake.ext import commands
from disnake.ext.commands import is_owner

import logging

logging = logging.getLogger("Dev")

class Dev(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def system_info(self, ctx):
        # Get system information
        system_info = {
            "Operating System": platform.system(),
            "Release Version": platform.release(),
            "CPU Usage": f"{psutil.cpu_percent()}%",
            "RAM Usage": f"{psutil.virtual_memory().percent}%",
            "Disk Usage": f"{psutil.disk_usage('/').percent}%",
        }

        # Create an embed to display the information
        embed = disnake.Embed(title="System Information", color=disnake.Color.blue())

        for key, value in system_info.items():
            embed.add_field(name=key, value=value, inline=False)

        await ctx.send(embed=embed)    
        
    @commands.command()
    async def sync(self, ctx):
        #try:
            os.system("git pull")
            embed = disnake.Embed(
                title="Success!!",
                description="I pulled and synced the repo, I\'m at the latest version.",
                color=disnake.dark_red()
            )
            ctx.send(embed=embed)
        #except:    
        

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def leave(self, ctx, *, guildinput):
        guildid = int(guildinput)
        guild = self.client.get_guild(guildid)
        await guild.leave()

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def servers(self, ctx):
        await ctx.send(f"{len(self.client.guilds)}")
        listofids = []
        for guild in self.client.guilds:
            listofids.append(guild.id)
        await ctx.send(listofids)
        
    @commands.command()
    async def crosscheck(self, ctx):
        list = [
            1210165420493905982,
            956054319529066527,
            956075132571508757,
            1171196139647803513,
            956210819325132921,
            956164930061619230,
            1185038257789079614,
            956246550152118374,
            956178931512410222,
            1172076548791226439,
            956037057157943377,
            1171219789738410037,
            956261113115336774,
            1172105789494792242,
            956131521733984287,
            1185042820009054312,
            1185050948675047539,
            1185047045413797898,
            1185037104523268189,
            1210170987073503265,
            956069338820001837,
            959468187328589845,
            1185046163473309696,
            1185046537944973383,
            1185046309976166460,
            1185047194261274665,
            956323664062722100,
            1185033314189443133,
            956202276408688650,
            1185045560273666170,
            1185033074304630936,
            1172086562176114689,
            1171223723714556015,
            1171197414632341508,
            1171223836973338634,
            956375867632799787,
            928350122843193385,
            956097947727179806,
            928586086828085358,
            956035417860362308,
            1210161585658798100,
            1185045337325449267,
            956119888991232050,
            1172080432389574690,
            932067526681186414,
            1185043970150117467,
            976786710836944936,
            1185047033183227947,
            1185045519576338442,
            1185034806908682281,
            1185047444619284641,
            932057102841708655,
            1185047344148918509,
            1185030898148724777,
            1185048077468450947,
            1185021551825920066,
            956080137932259398,
            956222023816847411,
            956137602564640799,
            956350881241104495,
            1185046383015760016,
            1185039817231323187,
            956128945227567145,
            956192794014269481,
            975468900244398151,
            1172073543836631040,
            1185039549991235654,
            956126507984637982,
            1185019322331045902,
            956092289552384010,
            1171227973450469426,
            1185045242706153573,
            1185036106257944677,
            1185036634270478406,
            956104664821157918,
            956172424309784617,
            1185043981785112728,
            974926574346440765,
            1185047968886308895,
            1185033301099020311,
            1185045436331982848,
            1171191966059466802,
            1185044083996098590,
            1185035242222923927,
            1171206094794797191,
            1185037967992037489,
            1172074070901264404,
            1171225487494893622,
            1185047092478095443,
            956131426250657862,
            956294250927120436,
            1185010648120303717,
            1185039045747818610,
            956173030218940486,
            978778806863151114,
            956153059371810836,
            928318741060673627,
            1185045420594974761,
            1185043681737179197,
            1185046791826178099,
            1185036303155335240,
            1185035279791292469,
            1185044808637616159,
            956292731880239176,
            932079867003039804,
            1185038081322135603,
            1185051129147555890,
            1171205707576660133,
            956237066503585873,
            1171204995392209047,
            1185047847557672993,
            1185039095211241552,
            1185047411605897301,
            1185038424101629962,
            956031608144666665,
            1185043232661450814,
            956200330251624468,
            956887823024275487,
            1210174835985088532,
            1210212474780127232,
            1185034487537606676,
            1185038000795680769,
            1185045871478448242,
            1185044716111265799,
            928483283698851901,
            1210158972280111164,
            1185047344023081011,
            923426902574759976,
            932084358326681662,
            956004017299927061,
            932094826059563040,
            928355373763674162,
            932096380879667253,
            923404990511480852,
            956157904539512874,
            95615790453951287
        ]
        await ctx.send("Starting crosscheck.")
        for member in ctx.guild.members:
            if member.id in list:
                await ctx.send (f"You need to ban {member.id}")
            else:
                return
        await ctx.send("Finished crosscheck.")

def setup(client):
    client.add_cog(Dev(client))

