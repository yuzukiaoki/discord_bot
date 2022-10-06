import discord
from discord.ext import commands
import json
import os,sys
from discord import Member
from data_file.get_something import *
#from data_file.keep_alive import keep_alive
from discord_slash import SlashCommand


with open('./mumi_setting.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

bot = commands.Bot(command_prefix='$')
bot.remove_command('help') #刪除內建的help指令
# slash指令
slash = SlashCommand(bot, sync_commands=True,  sync_on_cog_reload=True)

def is_it_me(ctx):
    return ctx.author.id == 268570448294945056


@bot.command()
@commands.check(is_it_me)
async def example(ctx):
    await ctx.send(f"hi im{ctx.author}")

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd,activity=discord.Streaming(name="輸入$help好嗎",
    url="https://www.youtube.com/channel/UC5Cw99Ml1eIgY8h02uZw7u8A"))
    print(">> Bot is online <<")

    takenGuild = bot.get_guild(3963830568926063474692) #必須在該伺服器才能get資訊
    get_server_id = get_server("https://api.jsonstorage.net/v1/json/cc3a38bc-d03a-43bd-b2dc-0d4127034cf1/17661465-b197-4dd4-a989-e3ffd4ce4d69?apiKey=a" #mix_json
                            ,"17661465-b197-4dd4-a989-e3ffd4ce4d69?apiKey="
                            ,"channel_info","channel_id")
    for channel in takenGuild.text_channels:
        if channel.id not in get_server_id:
            discord_upd("https://api.jsonstorage.net/v1/json/cc3a38bc-d03a-43bd-b2dc-0d4127034cf1/17661465-b197-4dd4-a989-e3ffd4ce4d69?apiKey=" #mix_json
            ,"17661465-b197-4dd4-a989-e3ffd4ce4d69?apiKey=",0,"channel_info",0,
            channel_guild = str(channel.guild), channel_name = channel.name, channel_id = channel.id
            ) # 2022/1/20發生 channel.guild 的type是 discord.guild.Guild object不能被寫到json 將他str化
        #channel.guild,channel.name,channel.id
        else:
            pass


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
    python = sys.executable #"F:\\python37\\python.exe" 原
    os.execl(python, python, * sys.argv) #在aws上不可使用

@bot.command()
async def restart(ctx):
    await ctx.message.delete()
    message = await ctx.send("Restarting... Allow up to 5 seconds")
    restart_program()

# @bot.command()
# async def add_channel(ctx, ch: int):  #在discord裡 新增channel id
#     channel = bot.get_channel(ch)
#     print(f"this is channel type {type(channel)}")
#     discord_upd("https://jsonstorage.net/api/items/0bb0a3f0-2274-4699-9834-4d9a9a027d19"
#             ,"0bb0a3f0-2274-4699-9834-4d9a9a027d19",0,"channel_info",1,
#             channel_guild = channel.guild, channel_name = channel.name, channel_id = ch
#             )
#     await ctx.send(f'add Channel:{channel.mention}')

for filename in os.listdir('./cmds'):
    if filename.endswith('.py'):
        bot.load_extension(f'cmds.{filename[:-3]}')
# keep_alive()

if __name__ == "__main__":
    bot.run(jdata['TOKEN'])


#git add .
#git commit -am "what do u want"
#git push heroku master


#如何打開setting.json(vscode的):ctrl+shift+p 搜尋setting 選擇開啟設定(JSON) (非工作區設定)
