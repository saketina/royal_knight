import disnake
from disnake.ext import commands
from disnake.ext.commands import guild_only
import json

import asyncio
import aiofiles
import time
import os

class Afk(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.afk_dict = {}

    @commands.Cog.listener()
    async def on_message(self, msg):
        # Afk System
        try:
            print("normal started")
            keys = self.afk_dict.keys()
            if str(msg.author.id) + str(msg.guild.id) in keys:
                """
                afk_end_embed = disnake.Embed(
                    title=f'[AFK] Disabled',
                    description=f'You\'re no longer afk. You had '
                                f'{len(self.afk_dict[str(msg.author.id) + str(msg.guild.id)])} mentions.\n'
                                'Check your DMs for the list of messages you were mentioned in. If you have your '
                                'DMs disabled, you can use the ``k.pingmessages`` command to check the message '
                    )
                await msg.channel.send(
                    embed=afk_end_embed, 
                    delete_after = 5
                    )
                """
                if len(self.afk_dict[str(msg.author.id) + str(msg.guild.id)]) < 1:
                    self.afk_dict.pop(str(msg.author.id) + str(msg.guild.id))
                    return
                afk_mention_list = ''
                for msg_info in self.afk_dict[str(msg.author.id) + str(msg.guild.id)]:
                    afk_mention_list += f'{msg_info}\n'
                afk_dm_embed = disnake.Embed(
                    title=f'AFK mention List',
                    description=afk_mention_list[:1999]
                    )
                afk_dm_embed.set_footer(
                    text='Download the File for full list of mentions'
                    )
                async with aiofiles.open(f'cogs/Assets/afk_mention_list_messages/{msg.author.id}.txt', 'w+') as f:
                    await f.write(
                        afk_mention_list
                        )
                    await f.flush()
                afk_list_file = disnake.File(f'cogs/Assets/afk_mention_list_messages/{msg.author.id}.txt',
                    'mentions.txt'
                    )
                await msg.author.send(embed=afk_dm_embed, file=afk_list_file)
                self.afk_dict.pop(str(msg.author.id) + str(msg.guild.id))
                await aiofiles.os.rmdir(f'cogs/Assets/afk_mention_list_messages/{msg.author.id}.txt')

            for mention in msg.mentions:
                key_id = str(mention.id) + str(msg.guild.id)
                if key_id in keys:
                    afk_reply_embed = disnake.Embed(
                        title=f'{mention.display_name} is currently afk',
                        description=f'**Reason**: {self.afk_dict["m"+key_id]}'
                        )
                    self.afk_dict[key_id].add(
                        f'Mentioned by: {msg.author.display_name}\n'
                        f'Message Content: {msg.content}\n'
                        f'Message Url: {msg.jump_url}\n'
                        )
                    await msg.channel.send(
                        embed=afk_reply_embed
                        )
        except disnake.Forbidden:
            print("forbiddden started")
            afk_mention_list = ''
            for msg_info in self.afk_dict[str(msg.author.id) + str(msg.guild.id)]:
                afk_mention_list += f'{msg_info}\n'
            afk_dm_embed = disnake.Embed(
                title=f'AFK mention List',
                description=afk_mention_list[:1999]
                )
            afk_dm_embed.set_footer(
                text='Download the File for full list of mentions'
                )
            async with aiofiles.open(f'cogs/Assets/afk_mention_list_messages/{msg.author.id}.txt', 'w+') as f:
                await f.write(
                    afk_mention_list
                    )
                await f.flush()
            afk_list_file = disnake.File(f'cogs/Assets/afk_mention_list_messages/{msg.author.id}.txt',
                'mentions.txt'
                )
            await msg.channel.send(embed=afk_dm_embed, file=afk_list_file)
            self.afk_dict.pop(str(msg.author.id) + str(msg.guild.id))
        except AttributeError as error:
            print(error.__traceback__)
        except KeyError as error:
            print(
                error.with_traceback(error.__traceback__)
                )
        except Exception as error:
            print(
                error.with_traceback(error.__traceback__)
                )
    
    @commands.command(pass_context=True)
    @commands.guild_only()
    async def afk(self, ctx, *, msg=""):
        await asyncio.sleep(3)
        self.afk_dict['m' + str(ctx.author.id) + str(ctx.guild.id)] = msg
        self.afk_dict[str(ctx.author.id) + str(ctx.guild.id)] = set([])
        afk_embed = disnake.Embed(
            description=f'{ctx.author.mention} You\'re now afk. 👌',
            color=disnake.Color.dark_red()
            )
        await ctx.send(embed=afk_embed)

def setup(client):
    client.add_cog(Afk(client))
    print(f"Cog: Afk - loaded.")

def teardown(client):
    print(f"Cog: Afk - unloaded.")