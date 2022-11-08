import disnake
from disnake.ext import commands

import typing
import random
from cogs.utils import emojis


class Actions(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.kiss_gifs = [
            "https://cdn.discordapp.com/attachments/724639524558471268/732156859238055936/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732156859712143413/image1.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732156860076916836/image2.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732156860349677618/image3.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732156860655992852/image4.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732156860957720596/image5.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732156863638011994/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732156863927418900/image1.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732156864434798704/image2.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732156864791445544/image3.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732156865210744893/image4.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732156865605271553/image5.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732156865911455825/image6.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732156866544664607/image7.gif",
        ]
        self.punch_gifs = [
            "https://cdn.discordapp.com/attachments/724639524558471268/732158497159905320/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732158497533460570/image1.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732158498045165649/image2.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732158498674311238/image3.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732158499186016296/image4.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732158499710304256/image5.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732158513387929600/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732158514079727646/image1.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732158514772049920/image2.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732158515430293534/image3.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732158516453965894/image4.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732158516789248030/image5.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732158517267529830/image6.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732158517967978547/image7.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732158518291070997/image8.gif",
        ]
        self.kill_gifs = [
            "https://cdn.discordapp.com/attachments/724639524558471268/732160843281858581/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732160843684380712/image1.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732160843927781396/image2.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732160844552732763/image3.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732160845135609886/image4.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732160845785858068/image5.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732160846238842940/image6.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732160846565998642/image7.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732160847023177808/image8.gif",
        ]
        self.pat_gifs = [
            "https://cdn.discordapp.com/attachments/724639524558471268/732582753241006110/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732582759201243216/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732582760103018657/image1.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732582760505409577/image2.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732582760891416627/image3.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732582761323298816/image4.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732582959030206565/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732582966999646278/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732582983529267290/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732582988621283368/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732583408726835290/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732583430600130620/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732583433942990971/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732583442784583690/image0.gif",
        ]
        self.smile_gifs = [
            "https://cdn.discordapp.com/attachments/724639524558471268/732587314907447356/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732587323606433872/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732587323388330014/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732587325195944066/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732587326219223121/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732587329214218260/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732587330552070235/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732587331999236136/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732587333857312828/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732587366929268766/image0.gif",
        ]
        self.nom_gifs = [
            "https://cdn.discordapp.com/attachments/724639524558471268/732591693349650552/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732591694431649792/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732591714291941436/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732591718016483389/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732591718297370744/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732591723389386830/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732591725994049636/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732591726484652152/image1.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732591735548674098/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732591737205424208/image0.gif",
        ]
        self.slap_gifs = [
            "https://cdn.discordapp.com/attachments/724639524558471268/732596821313978449/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732596824996839546/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732596838867402772/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732596848937926715/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732596850376441886/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732596850636488815/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732596861030105138/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732596865669005362/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732596867589734480/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732596879589638285/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732596879862399056/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732596881485594634/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732596889177817158/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732596895691571208/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732596905099657306/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732596906974511164/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732596907733680208/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732596908614483988/image0.gif",
        ]
        self.hug_gifs = [
            "https://cdn.discordapp.com/attachments/724639524558471268/732598260425818212/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732598275445751878/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732598276154720337/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732598276406247504/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732598278801195088/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732598284379488256/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732598297675563038/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732598307326787604/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732598723078783036/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732598723498082424/image1.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/732598723879895074/image2.gif",
        ]
        self.cry_gifs = [
            "https://cdn.discordapp.com/attachments/724639524558471268/743023802547699782/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743023815226818601/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743023817256992837/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743023819790483476/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743023823863021568/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743023829026078770/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743023838077649026/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743023842368159804/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743023848055635988/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743023956751155280/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743023987042287616/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743024001915289660/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743024018335989760/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743024022840672326/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743024031833391134/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743024047058714644/image0.gif",
        ]
        self.cuddle_gifs = [
            "https://cdn.discordapp.com/attachments/724639524558471268/743027622593953864/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743027638737567794/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743027640201641994/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743027641011011654/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743027642093142096/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743027644345352202/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743027644945268746/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743027649718386798/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743027651186524230/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743027652968972328/image0.gif",
        ]
        self.dance_gifs = [
            "https://cdn.discordapp.com/attachments/724639524558471268/743030434484584458/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743030441422094396/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743030447134736384/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743030455959420968/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743030472686436412/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743030476385550436/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743030484090617906/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743030485524938802/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743030494849138738/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743030498485600298/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743030498783133746/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743030517573615676/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743030517636661368/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743030520593645568/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743030526369333298/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743030532614651954/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743030566152175616/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743030611714768936/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743030625342324836/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743030669814399036/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743030673752850452/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743030704614408242/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743030711707107348/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743030756225318932/image0.gif",
            "https://cdn.discordapp.com/attachments/724639524558471268/743030769600954438/image0.gif",
        ]

    @commands.command()
    async def kiss(self, ctx, member: typing.Optional[disnake.Member]):
        if member is None or member == ctx.author:
            target = "themselves"
        else:
            target = member.display_name

        kiss_embed = disnake.Embed(
            title="",
            description=f"{ctx.author.display_name} kisses {target}",
        )
        kiss_embed.set_image(url=random.choice(self.kiss_gifs))

        await ctx.send(embed=kiss_embed)

    @commands.command()
    async def punch(self, ctx, member: typing.Optional[disnake.Member]):
        if member is None or member == ctx.author:
            target = "themselves"
        else:
            target = member.display_name

        punch_embed = disnake.Embed(
            title="",
            description=f"{ctx.author.display_name} punches {target}",
        )
        punch_embed.set_image(url=random.choice(self.punch_gifs))

        await ctx.send(embed=punch_embed)

    @commands.command()
    async def kill(self, ctx, member: typing.Optional[disnake.Member]):
        if member is None or member == ctx.author:
            target = "themselves"
        else:
            target = member.display_name

        kill_embed = disnake.Embed(
            title="",
            description=f"{ctx.author.display_name} kills {target}",
        )
        kill_embed.set_image(url=random.choice(self.kill_gifs))

        await ctx.send(embed=kill_embed)

    @commands.command()
    async def pat(self, ctx, member: typing.Optional[disnake.Member]):
        if member is None or member == ctx.author:
            target = "themselves"
        else:
            target = member.display_name
        pat_embed = disnake.Embed(
            title="",
            description=f"{ctx.author.display_name} pats {target}",
        )
        pat_embed.set_image(url=random.choice(self.pat_gifs))

        await ctx.send(embed=pat_embed)

    @commands.command()
    async def smile(self, ctx, member: typing.Optional[disnake.Member]):
        if member is None or member == ctx.author:
            target = "themselves"
        else:
            target = member.display_name

        smile_embed = disnake.Embed(
            title="",
            description=f"{ctx.author.display_name} smile to {target}",
        )
        smile_embed.set_image(url=random.choice(self.smile_gifs))

        await ctx.send(embed=smile_embed)

    @commands.command()
    async def nom(self, ctx, member: typing.Optional[disnake.Member]):
        if member is None or member == ctx.author:
            target = "themselves"
        else:
            target = f"{member.display_name}"

        nom_embed = disnake.Embed(
            title="",
            description=f"{ctx.author.display_name} noms on {target}.",
        )
        nom_embed.set_image(url=random.choice(self.nom_gifs))

        await ctx.send(embed=nom_embed)

    @commands.command()
    async def slap(self, ctx, member: typing.Optional[disnake.Member]):
        if member is None or member == ctx.author:
            target = "themselves"
        else:
            target = f"{member.display_name}"

        slap_embed = disnake.Embed(
            title="",
            description=f"{ctx.author.display_name} slaps {target}.",
        )
        slap_embed.set_image(url=random.choice(self.slap_gifs))

        await ctx.send(embed=slap_embed)

    @commands.command()
    async def hug(self, ctx, member: typing.Optional[disnake.Member]):
        if member is None or member == ctx.author:
            target = "themselves"
        else:
            target = f"{member.display_name}"

        hug_embed = disnake.Embed(
            title="",
            description=f"{ctx.author.display_name} hugs {target}.",
        )
        hug_embed.set_image(url=random.choice(self.hug_gifs))

        await ctx.send(embed=hug_embed)

    @commands.command()
    async def cry(self, ctx, member: typing.Optional[disnake.Member]):
        if member is None or member == ctx.author:
            target = "themselves"
        else:
            target = f"{member.display_name}"

        cry_embed = disnake.Embed(
            title="",
            description=f"{ctx.author.display_name} cries to {target}.",
        )
        cry_embed.set_image(url=random.choice(self.cry_gifs))

        await ctx.send(embed=cry_embed)

    @commands.command()
    async def cuddle(self, ctx, member: typing.Optional[disnake.Member]):
        if member is None or member == ctx.author:
            target = "themselves"
        else:
            target = f"{member.display_name}"

        cuddle_embed = disnake.Embed(
            title="",
            description=f"{ctx.author.display_name} cuddles {target}.",
        )
        cuddle_embed.set_image(url=random.choice(self.cuddle_gifs))

        await ctx.send(embed=cuddle_embed)

    @commands.command()
    async def dance(self, ctx, member: typing.Optional[disnake.Member]):
        if member is None or member == ctx.author:
            target = "themselves"
        else:
            target = f"{member.display_name}"

        dance_embed = disnake.Embed(
            title="",
            description=f"{ctx.author.display_name} dances with {target}.",
        )
        dance_embed.set_image(url=random.choice(self.dance_gifs))

        await ctx.send(embed=dance_embed)


def setup(client):
    client.add_cog(Actions(client))
