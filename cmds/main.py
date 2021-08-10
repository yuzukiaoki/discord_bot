import discord
from discord.ext import commands
from core.classes import Cog_Extension
import datetime
from datetime import tzinfo, timedelta, datetime, timezone

class Main(Cog_Extension):

    @commands.command() 
    async def ping(self, ctx):
        await ctx.send(f'{round(self.bot.latency*1000)}(ms)')

    @commands.command()
    async def hi(self, ctx):
        await ctx.send(':thinking: ')  #命令 範例
    
    @commands.command()
    async def 踩地雷(self, ctx): #兩個|| 包圍字符 會隱藏該字
        await ctx.send('||:zero:|| ||:one:|| ||:boom:|| ||:one:|| ||:zero:|| ||:one:|| ||:boom:|| ||:one:||\n'+
'||:zero:|| ||:one:|| ||:one:|| ||:one:|| ||:zero:|| ||:one:|| ||:two:|| ||:two:||\n'+
'||:zero:|| ||:zero:|| ||:zero:|| ||:zero:|| ||:one:|| ||:one:|| ||:two:|| ||:boom:||\n'+
'||:zero:|| ||:zero:|| ||:zero:|| ||:zero:|| ||:one:|| ||:boom:|| ||:three:|| ||:two:||\n'+
'||:zero:|| ||:zero:|| ||:one:|| ||:one:|| ||:three:|| ||:three:|| ||:boom:|| ||:one:||\n'+
'||:zero:|| ||:one:|| ||:three:|| ||:boom:|| ||:three:|| ||:boom:|| ||:two:|| ||:one:||\n'+
'||:zero:|| ||:one:|| ||:boom:|| ||:boom:|| ||:four:|| ||:two:|| ||:one:|| ||:zero:||\n'+
'||:zero:|| ||:one:|| ||:two:|| ||:three:|| ||:boom:|| ||:one:|| ||:zero:|| ||:zero:||') 
    @commands.command()
    async def 踩地雷2(self, ctx):
        await ctx.send('||:one:||   ||:boom:||   ||:two:||   ||:boom:||   ||:one:||   ||:zero:||   ||:zero:||   ||:zero:||   ||:zero:||\n'+ 
'||:two:||   ||:three:||   ||:four:||   ||:three:||   ||:two:||   ||:zero:||   ||:zero:||   ||:one:||   ||:one:||\n'+ 
'||:boom:||   ||:three:||   ||:boom:||   ||:boom:||   ||:two:||   ||:two:||   ||:two:||   ||:two:||   ||:boom:||\n'+ 
'||:two:||   ||:boom:||   ||:three:||   ||:three:||   ||:three:||   ||:boom:||   ||:boom:||   ||:two:||   ||:one:||\n'+ 
'||:one:||   ||:two:||   ||:two:||   ||:two:||   ||:boom:||   ||:four:||   ||:three:||   ||:one:||   ||:zero:||\n'+ 
'||:zero:||   ||:one:||   ||:boom:||   ||:two:||   ||:two:||   ||:boom:||   ||:one:||   ||:one:||   ||:one:||\n'+ 
'||:zero:||   ||:one:||   ||:one:||   ||:one:||   ||:one:||   ||:one:||   ||:two:||   ||:two:||   ||:boom:||\n'+ 
'||:one:||   ||:one:||   ||:one:||   ||:zero:||   ||:zero:||   ||:zero:||   ||:one:||   ||:boom:||   ||:two:||\n'+ 
'||:one:||   ||:boom:||   ||:one:||   ||:zero:||   ||:zero:||   ||:zero:||   ||:one:||   ||:one:||   ||:one:||')
    @commands.command()
    async def em(self, ctx): #顯示機器人狀態表
        embed=discord.Embed(title="dragon", url="https://www.youtube.com/watch?v=CD9VhYwJDP8", description="<:dragon2:697874243232202823> ", color=0x9256c2, 
        timestamp= datetime.now(timezone.utc)) #原為datetime.datetime.now() / 更該後可顯示當前時區
        embed.set_author(name="just a dragon", url="https://www.youtube.com/watch?v=CD9VhYwJDP8", 
        icon_url="https://media.discordapp.net/attachments/708892923420213288/713377203894747156/1069461.gif")
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/708892923420213288/713377203894747156/1069461.gif")
        embed.add_field(name="身長", value="10m", inline=True)
        embed.add_field(name="體重", value="8787kg", inline=True)
        embed.add_field(name="喜好", value="雜食性", inline=True)
        embed.set_footer(text="balabala  "+ctx.message.author.name)
        await ctx.send(embed=embed)

    @commands.command()
    async def sayd(self, ctx, *, msg): #讓機器人附送發言者發言
        await ctx.message.delete()
        await ctx.send(msg)
    
    @commands.command()
    async def clean_admin(self, ctx, num:int): #刪除聊天室發言，包含機器人
        await ctx.channel.purge(limit=num+1)  #注意 機器人必須要有刪除留言的權限
    
    @commands.command()
    async def clean(self,ctx,num:int): #刪除聊天室發言，不包含機器人
        await ctx.channel.purge(limit=num+1,check=lambda m: m.author == self.bot.user)


def setup(bot):
    bot.add_cog(Main(bot))
