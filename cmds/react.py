import discord
from discord import client
from discord.ext import commands
from discord.ext.commands import bot
from core.classes import Cog_Extension
import random, asyncio
import json
import datetime
from datetime import tzinfo, timedelta, datetime, timezone
from data_file import *
from data_file.get_something import discord_upd, get_server

with open('mumi_setting.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

class React(Cog_Extension):
    @commands.command()
    async def 圖片(self,ctx):
        random_pic = random.choice(jdata['pic'])
        pic = discord.File(random_pic)
        await ctx.send(file= pic)

    @commands.command()
    async def web(self,ctx):
        random_pic = random.choice(jdata['url_pic'])
        await ctx.send(random_pic)
    
    @commands.is_owner()
    @commands.command()
    async def 時間(self,ctx):
        tz = timezone(timedelta(hours=+8)) #utc+8 變為台灣時區
        now_time = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
        await ctx.send(f"現在時間{now_time}")

    @commands.command()
    async def 十三(self,ctx):
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
        await ctx.channel.send(f"{random_old}  by{ctx.author.name}")

    @commands.command()
    async def add_user(self, ctx, ch:int): #增加使用者

        # @ + Aoki#9240 就會抓到那個人目前的名字 ，我抓的'name' 必須+@ 才能知道現在他的名字
        user = await self.bot.fetch_user(ch)
        #print(f"this is self.user {type(user)}")
        user_list = get_server(
    "https://api.jsonstorage.net/v1/json/cc3a38bc-d03a-43bd-b2dc-0d4127034cf1/17661465-b197-4dd4-a989-e3ffd4ce4d69?apiKey=a" #mix_json
    ,"17661465-b197-4dd4-a989-e3ffd4ce4d69?apiKey=","bot_user","bot_user_id")
        if ch not in user_list:
            discord_upd("https://api.jsonstorage.net/v1/json/cc3a38bc-d03a-43bd-b2dc-0d4127034cf1/17661465-b197-4dd4-a989-e3ffd4ce4d69?apiKey=" #mix_json
    ,"17661465-b197-4dd4-a989-e3ffd4ce4d69?apiKey=",0,"bot_user",0,
    bot_user_name=str(user), bot_user_id=ch) #user的type不能存入json 要str化
            await ctx.send(f'新增的使用者:{user.mention}, 名字:{user} / {user.name}')
        elif ch in user_list:
            await ctx.send('已經有這個使用者了啦 哭阿')
        else:                                           #user.name不會有後面的序號
            await ctx.send('新增失敗或是有例外狀況 o_<')
   
    @commands.command()
    async def delete_user(self, ctx, id:int): #刪除使用者
        del_user = await self.bot.fetch_user(id)
        user_list = get_server(
    "https://api.jsonstorage.net/v1/json/cc3a38bc-d03a-43bd-b2dc-0d4127034cf1/17661465-b197-4dd4-a989-e3ffd4ce4d69?apiKey=" #mix_json
    ,"17661465-b197-4dd4-a989-e3ffd4ce4d69?apiKey=","bot_user","bot_user_id")
        if id in user_list:
            discord_upd("https://api.jsonstorage.net/v1/json/cc3a38bc-d03a-43bd-b2dc-0d4127034cf1/17661465-b197-4dd4-a989-e3ffd4ce4d69?apiKey=" #mix_json
    ,"17661465-b197-4dd4-a989-e3ffd4ce4d69?apiKey=",0,"bot_user",1 , id,'bot_user_id')
            await ctx.send(f'刪除使用者:{del_user.mention}, 名字:{del_user} / {del_user.name}')
        elif id not in user_list:
            await ctx.send('沒有這個人R <:doge2:741336412091056218>')
        else:                                          
            await ctx.send('新增失敗或是有例外狀況 o_<')
        
    @commands.command()
    async def add_channel(self, ctx, ch: int):  #在discord裡 新增channel id
        channel = self.bot.get_channel(ch)
        #print(f"this is channel type {type(channel)}")
        channel_list = get_server(
        "https://api.jsonstorage.net/v1/json/cc3a38bc-d03a-43bd-b2dc-0d4127034cf1/17661465-b197-4dd4-a989-e3ffd4ce4d69?apiKey=" #mix_json
        ,"17661465-b197-4dd4-a989-e3ffd4ce4d69?apiKey=","channel_info","channel_id")
        if ch not in channel_list:
            discord_upd("https://api.jsonstorage.net/v1/json/cc3a38bc-d03a-43bd-b2dc-0d4127034cf1/17661465-b197-4dd4-a989-e3ffd4ce4d69?apiKey=" #mix_json
                    ,"17661465-b197-4dd4-a989-e3ffd4ce4d69?apiKey=",0,"channel_info",0,
                    channel_guild = channel.guild, channel_name = channel.name, channel_id = ch
                    )
            await ctx.send(f'add Channel:{channel.mention}')
        elif ch  in channel_list:
            await ctx.send('你加過這頻道了啦 <:doge2:741336412091056218>')
        else:                                          
            await ctx.send('新增失敗或是有例外狀況 o_<')

    @commands.command()
    async def del_channel(self, ctx, ch: int):  #在discord裡 刪除channel id
        channel = self.bot.get_channel(ch)
        channel_list = get_server(
        "https://api.jsonstorage.net/v1/json/cc3a38bc-d03a-43bd-b2dc-0d4127034cf1/17661465-b197-4dd4-a989-e3ffd4ce4d69?apiKey=" #mix_json
        ,"17661465-b197-4dd4-a989-e3ffd4ce4d69?apiKey=","channel_info","channel_id")
        if ch in channel_list:
            discord_upd("https://api.jsonstorage.net/v1/json/cc3a38bc-d03a-43bd-b2dc-0d4127034cf1/17661465-b197-4dd4-a989-e3ffd4ce4d69?apiKey=" #mix_json
                    ,"17661465-b197-4dd4-a989-e3ffd4ce4d69?apiKey=",0,"channel_info",1 , ch,'channel_id')
            await ctx.send(f'delete Channel:{channel.mention}')
        elif ch  not in channel_list:
            await ctx.send('沒有這頻道R <:doge2:741336412091056218>')
        else:                                          
            await ctx.send('新增失敗或是有例外狀況 o_<')


    @commands.command()
    async def quiz(self,ctx):
        """
        #還想不到能幹嘛 先擺著
        使用者輸入$quiz
        機器人會問填入A或B或C
        依據使用者輸入的答案
        執行相對應的結果
        """
        await ctx.send("A, B or C")

        try:
            msg = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30.0)

        except asyncio.TimeoutError:
            await ctx.send("You took to long...")

        else:
            if msg.content == "A":
                await ctx.send("Correct")
            elif msg.content == "B":
                await ctx.send("Wrong")
            elif msg.content == "C":
                await ctx.send("Wrong")
            else:
                await ctx.send("Huh?")

def setup(bot):
    bot.add_cog(React(bot))
