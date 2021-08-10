import discord
from discord.ext import commands
from core.classes import Cog_Extension
import random
import json
import datetime
from datetime import tzinfo, timedelta, datetime, timezone

with open('setting.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

class React(Cog_Extension):
    @commands.command()
    async def 圖片(self,ctx): #隨機叫出圖片
        random_pic = random.choice(jdata['pic'])
        pic = discord.File(random_pic)
        await ctx.send(file= pic)

    @commands.command()
    async def web(self,ctx): #隨機叫出圖片
        random_pic = random.choice(jdata['url_pic'])
        await ctx.send(random_pic)
    
    @commands.command()
    async def 時間(self,ctx): #當前時間
        tz = timezone(timedelta(hours=+8)) #utc+8 變為台灣時區
        now_time = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
        await ctx.send(f"現在時間{now_time}")

    @commands.command()
    async def 十三(self,ctx): #以下為個人餘興
        await ctx.send("噁")

    @commands.command()
    async def SOP(self,ctx):
        random_SOP_random = random.choice(jdata['SOP_random'])
        await ctx.channel.send(random_SOP_random)

    @commands.command()
    async def sop(self,ctx):
        random_sop_random = random.choice(jdata['sop_random'])
        await ctx.channel.send(random_sop_random)

    @commands.command()
    async def 少年(self,ctx):
        random_old = random.choice(jdata['old'])
        await ctx.channel.send(random_old)


def setup(bot):
    bot.add_cog(React(bot))
