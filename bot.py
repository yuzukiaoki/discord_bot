import discord
from discord.ext import commands
import json
import random,requests
import os,time,sys
from discord.utils import get
from discord import Member


with open('./setting.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

bot = commands.Bot(command_prefix='$') # 呼叫bot指令 前面加上 $


def is_it_me(ctx):
    return ctx.author.id == 268570448294445056 

def channel_append(channel_guild,channel_name,channel_id,address,ad_id,num,n_key):
            response = requests.get(address,{"id":ad_id}) 

            data = response.json()
            #回傳給json如個是字串 要用f"{}"包起來 
            content = {"channel_guild":f"{channel_guild}","channel_name":f"{channel_name}","channel_id":channel_id}
            #if channel_id not in server_info(num,n_key,channel_id,address,ad_id):
            data[num][n_key].append(content)
            # else:
            #     pass
            return data

def upd_server(up_guild,up_name,up_id,address,ad_id,num,n_key):    #上傳至雲端json
            update = requests.put(address,
            params =   {"id":ad_id},
            json = channel_append(up_guild,up_name,up_id,address,ad_id,num,n_key)
            )


@bot.command()
@commands.check(is_it_me)
async def example(ctx):
    await ctx.send(f"hi im{ctx.author}")

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd,activity=discord.Game('期間限定手套襪子'))
    print(">> Bot is online <<")
    
    takenGuild = bot.get_guild(396383026063474692) #必須在該伺服器才能get資訊
    for channel in takenGuild.text_channels:    #啟動bot同時 抓取指定伺服器裡所有頻道，上傳至資料庫
        upd_server(channel.guild,channel.name,channel.id
        ,"https://jsonstorage.net/api/items/0bb0a3f0-2274-4699-9834-4d9a9a027d19"
        ,"0bb0a3f0-2274-4699-9834-4d9a9a027d19",0,"channel_info")


@bot.command()
async def load(ctx,extension):
    bot.load_extension(f'cmds.{extension}')
    await ctx.send(f'Loaded {extension} done.')

@bot.command()
async def unload(ctx,extension):
    bot.unload_extension(f'cmds.{extension}')
    await ctx.send(f'Un - Loaded {extension} done.')  

@bot.command()
async def reload(ctx,extension):
    bot.reload_extension(f'cmds.{extension}')
    await ctx.send(f'Re - Loaded {extension} done.') 

@bot.command(pass_context=True, name='status')
async def status(ctx, member: Member):
    await ctx.send(str(member.status))
#確認status ，用法:!status 暱稱


def restart_program():
    python = sys.executable 
    os.execl(python, python, * sys.argv) #在aws上不可使用

@bot.command()
async def restart(ctx):
    await ctx.message.delete() #指令重啟bot heroku上可使用
    message = await ctx.send("Restarting... Allow up to 5 seconds")
    restart_program()

@bot.command()
async def add_channel(ctx, ch: int):  #手動新增可使用指令的頻道
    channel = bot.get_channel(ch)
    upd_server(channel.guild,channel.name,ch
    ,"https://jsonstorage.net/api/items/0bb0a3f0-2274-4699-9834-4d9a9a027d19"
    ,"0bb0a3f0-2274-4699-9834-4d9a9a027d19",0,"channel_info")
    await ctx.send(f'add Channel:{channel.mention}')

for filename in os.listdir('./cmds'):
    if filename.endswith('.py'):
        bot.load_extension(f'cmds.{filename[:-3]}')

if __name__ == "__main__":
    bot.run(jdata['TOKEN'])  #token上傳到公開git會被discord改掉，故先行刪除





#如何打開setting.json(vscode的):ctrl+shift+p 搜尋setting 選擇開啟設定(JSON) (非工作區設定)
