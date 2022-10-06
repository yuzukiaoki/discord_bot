import discord, json, random
#from discord.ext import commands
#from discord import guild
from discord_slash import SlashContext,cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option
from core.classes import Cog_Extension
import datetime
from datetime import datetime, timezone

with open('mumi_setting.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)


class slash(Cog_Extension):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @cog_ext.cog_slash(name="lovelyBird",description="雞") #name不能有空白 descri可以
    async def _slash_bird(self, ctx: SlashContext):
        await ctx.send(content=random.choice(jdata['bird']))

    @cog_ext.cog_slash(name="dragon",description="blue socks")
    async def _slash_dragon(self, ctx: SlashContext):
        embed = discord.Embed(
            title="點我獲取更多恐龍", 
            url="https://www.youtube.com/watch?v=CD9V4hY577wJDP8", 
            description="手套襪子AKA你今晚的噩夢",
            color=0x9256c2, 
            timestamp= datetime.now(timezone.utc))
        embed.set_author(name="海龍王彼得", url="https://www.youtube.com/watch?v=CD95757VhYwJDP8", 
        icon_url="https://cdn.discordapp.com/attachments/744467876999856132/74633517575796059664481/gifmagazine_1.gif")
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/7088929232424420213288/713377203894747156/1069461.gif")
        embed.add_field(
            name="$ping",
            value="你Ping阿",
            inline=False
            )
        embed.add_field(
            name="$hi",
            value="Hello",
            inline=False
            )
        embed.add_field(
            name="$踩地雷",
            value="0.0",
            inline=False
            )
        embed.add_field(
            name="踩地雷2",
            value="哪次不踩",
            inline=False
            )
        embed.add_field(
            name="$em",
            value="可撥恐龍",
            inline=False
            )
        embed.add_field(
            name="$SOP",
            value="?_?",
            inline=False
            )
        embed.add_field(
            name="$sop",
            value="surprise mothxx fuxxxx",
            inline=False
            )
        embed.add_field(
            name="$web",
            value="o_<",
            inline=False
            )
        # embed = discord.Embed(title="embed test")
        await ctx.send(embeds=[embed])

    @cog_ext.cog_slash(name="Asiagodtone",description="奶酪")
    async def _slash_Tommy(self, ctx: SlashContext):
        await ctx.send(content=random.choice(jdata['Tommy']))

    @cog_ext.cog_slash(
    name="secretCommand", #不能有空白
    description="你說...甚麼",
    options=[
        create_option(
            name="option", #不能變名稱
            description="選一個",
            required=True,
            option_type=3, #這到底是啥
            choices=[
                create_choice(
                    name="這是甚麼",
                    value="我　要　了",
                ),
                create_choice(
                    name="Any Idea?", #可以有空白
                    value="https://tenor.com/view/%E5%AD%94%E6%98%8E%E8%88%9E01-gif-252427360801",
                ),
            ]
        )
    ])
    async def _slash_option(self, ctx: SlashContext, option:str):
        await ctx.send(option)



def setup(bot):
    bot.add_cog(slash(bot))