from discord.ext import commands
from core.classes import Cog_Extension
import json
import asyncio
from datetime import timedelta
from data_file import *
from data_file.get_something import set_timeznoe, em, scrape_interval

class Task(Cog_Extension):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.add_twTime = timedelta(minutes=480) # 原本是 datime.timedelta ，2021/12/22重新push上去後 卻說不行，所以改成只有timedelta
        self.check_time = set_timeznoe(8).strftime('%H:%M:%S')  # 時間確認

        # 似乎不需要特別設定變數 selfXXX = selfXXX loop 
        # self.access = self.bot.loop.create_task(self.variable()) # 執行取得全域變數

        #self.bg_task  = self.bot.loop.create_task(self.loop_send_msg()) #每29分推播
        self.bot.loop.create_task(self.time_task()) #報時ㄐㄐ人

        self.bot.loop.create_task(scrape_interval(self.bot, 87822186214537669765130, 'bh3', '1'
        ,"https://api.jsonstorage.net/v1/json/cc3a38bc-d03a-43bd-b2dc-0d4127034cf1/67d50f93-c2e7-4d1a-905c-333d4625a19a?apiKey="
        ,"67d50f93-c2e7-4d1a-905c-333d4625a19a?apiKey=", "honkai_id", "honkai", title=" Impact")) #崩壞FB

        self.bot.loop.create_task(scrape_interval(self.bot, 849268997327371987054663, 'wans.com.tw', '2'
        ,"https://api.jsonstorage.net/v1/json/cc3a38bc-d03a-43bd-b2dc-0d4127034cf1/857bd6f1-04f1-4524-ad5a-2ad16f14f19d?apiKey="
        ,"857bd6f1-04f1-4524-ad5a-2ad16f14f19d?apiKey=", "maple_id", "maple", title=" Story")) #maple FB
       
        self.bot.loop.create_task(scrape_interval(self.bot, 933561123246528681549916, 'azW', '3'
        ,"https://api.jsonstorage.net/v1/json/cc3a38bc-d03a-43bd-b2dc-0d4127034cf1/12c72c0e-0c44-4a7c-9b3c-67e6eb1955f6?apiKey="
        ,"12c72c0e-0c44-4a7c-9b3c-67e6eb1955f6?apiKey=", "azure_id", "azure", title=" Lane")) #碧藍FB

    # async def variable(self):
    #     """
    #     跟self.bot相關 全域變數放這裡
    #     不知道為什麼self.bot.loop.create_task可以放上面
    #     """
    #     await self.bot.wait_until_ready()
    #     self.error_channel = self.bot.get_channel(1014227437846434782306304) # 錯誤回報頻道

    async def time_task(self):
        await self.bot.wait_until_ready()  # 等待bot 啟動完畢
        while not self.bot.is_closed():  # 如果bot沒有關閉的話 就一直loop

            now_time = set_timeznoe(8).strftime('%H:%M')  # 原為datetime.datetime.now()
            with open('mumi_setting.json', 'r', encoding='utf8') as jfile:
                jdata = json.load(jfile)
            dragon_channel = self.bot.get_channel(jdata['time_task_channel'])
            #print("(39)恐龍報時頻道: ",self.channel)
            if now_time == jdata['time']:

                await em(dragon_channel)
                await asyncio.sleep(80000)
            else:
                await asyncio.sleep(30)
                pass



    @commands.command()
    async def set_channel(self, ctx, ch: int):  # ch 頻道的參數
        self.channel = self.bot.get_channel(ch)
        await ctx.send(f'Set Channel:{self.channel.mention}')  # .mation 提及

    @commands.command()
    async def set_time(self, ctx, time):
       # self.counter = 0
        with open('mumi_setting.json', 'r', encoding='utf8') as jfile:
            jdata = json.load(jfile)
        await ctx.send("定時成功")

        jdata['time'] = time  # 使用者輸入的time傳入到jdata
        with open('mumi_setting.json', 'w', encoding='utf8') as jfile:  # w = 寫入
            json.dump(jdata, jfile, indent=4, ensure_ascii=False)  # indent 縮排

    

# __________註解終止線__________
def setup(bot):
    bot.add_cog(Task(bot))



