import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json, os, time
import asyncio
import datetime
import random
from datetime import tzinfo, timedelta, timezone
from facebook_scraper import get_posts
from cmds.event import ComplexEncoder
import sys,traceback,requests
from datetime import datetime as dt



class Task(Cog_Extension):


    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
  

        async def time_task():              #機器人將在指定時間 定時發送文字
            tz = timezone(timedelta(hours=+8))
            await self.bot.wait_until_ready()  # 等待bot 啟動完畢
            while not self.bot.is_closed():  # 如果bot沒有關閉的話 就一直loop
                now_time = dt.now(tz).strftime('%H:%M:%S')  # 原為datetime.datetime.now()
                with open('setting.json', 'r', encoding='utf8') as jfile:
                    jdata = json.load(jfile)
                self.channel = self.bot.get_channel(jdata['time_task_channel'])
                #print("(39)恐龍報時頻道: ",self.channel)
                if now_time == jdata['time']:
                    random_soldier = random.choice(jdata['soldier'])
                    #await self.channel.send('現在時間05:30:00，洞伍三洞，部隊起床，洞伍伍洞操場集合完畢')
                    await self.channel.send(random_soldier)
                    await asyncio.sleep(80000) #指定時間發完文字 立即進入冷卻80000秒
                else:
                    await asyncio.sleep(1)
                    pass

        self.bg_task = self.bot.loop.create_task(time_task())

        async def interval():  # 取名稱作 interval
            await self.bot.wait_until_ready()  # 等待bot 啟動完畢
            self.counter = 0 
            while not self.bot.is_closed():
                await asyncio.sleep(10)  # 這次行動要睡多久
                try: #try迴圈 避免網路或其他錯誤導致程式中指
                    await asyncio.sleep(30) #休息30秒
                    try_count = 0
                    while True:
                        try:                        #抓取azurlaneTW粉絲團 pages=2 僅閱覽兩頁的FB #cookies 將FB帳號存成cookie，可使用1年，#使用cookies避免FB需登入才可看文章問題
                            article_list = get_posts('azurlaneTW', pages=2,cookies='cookie.json')  # 得到文章列表       #由於機器人架在AWS，FB帳號必須改為英文介面
                            await asyncio.sleep(10)                       #cookies 因隱私問題 已從資料夾內刪除                                        
                            print("azure_try_count = ",try_count) #顯示重試次數
                        except Exception as ex:
                            await asyncio.sleep(10) #爬蟲失敗 等待10秒
                            print("Exception happend",ex)
                            try_count +=1  
                        else:
                            for post in article_list: #post time +480分鐘 => 8小時時區
                                alltext = f"{(post['time']+datetime.timedelta(minutes=480)).strftime('%Y-%m-%d %H:%M:%S')}\n{ post['text'][:800]}\n{ post['post_url']}"

                                await asyncio.sleep(15)  # 冷卻 沒有BOT啟動不了
                                print("Azure outer counter = ",self.counter)  #↓time改成id
                                if f"{post['post_id']}" not in time_list("azure_id"        #與資料庫的 文章發文時間比對，避免重複抓取同樣文章
                                ,"https://jsonstorage.net/api/items/4cce38d5-01b0-44e4-a01e-eb573fb419a2"
                                ,"4cce38d5-01b0-44e4-a01e-eb573fb419a2")[0] and self.counter < 3:  #一個循環最多抓取三次文章
                                    self.azure_channel = self.bot.get_channel(822153105881694308)
                                    await self.azure_channel.send(alltext) #紛絲團PO文 傳送到discord聊天室
                                    await asyncio.sleep(2)
                                    for image in post['images']: #把images裡所有的圖一個一個列印出來
                                        await self.azure_channel.send(f"\n{image}") 
                                        await asyncio.sleep(2) #放個CD避免URL擠成一團
                                    self.counter += 1
                                    print("Azure inside counter = ",self.counter)
                                    upd(f"{post['post_id']}",f"{post['time'].strftime('%H:%M:%S')}",
                                    'https://jsonstorage.net/api/items/4cce38d5-01b0-44e4-a01e-eb573fb419a2',
                                    "4cce38d5-01b0-44e4-a01e-eb573fb419a2","azure") #新增並上傳資料庫
                                    await asyncio.sleep(10)
                                elif self.counter == 3:
                                    self.counter = 0
                                  
                                    break
                                else:
                                    self.counter += 1
                                    await asyncio.sleep(20)
                           
                            break  #出問題 再改break位置 
                    self.counter = 0
                    tz = timezone(timedelta(hours=+8))
                    check_time = dt.now(tz).strftime('%H:%M:%S')  # 時間確認
                    print("Azure Now Time : ", check_time)         
                    await asyncio.sleep(5)
                    print("Azure Zzzzz....( ´ ▽ ` )ﾉ")  
                    await asyncio.sleep(2700) #此循環 每2700秒執行一次

                except Exception as e: #印出錯誤狀況
                        error_class = e.__class__.__name__ #取得錯誤類型
                        detail = e.args[0] #取得詳細內容
                        cl, exc, tb = sys.exc_info() #取得Call Stack
                        lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
                        fileName = lastCallStack[0] #取得發生的檔案名稱
                        lineNum = lastCallStack[1] #取得發生的行號
                        funcName = lastCallStack[2] #取得發生的函數名稱
                      #  print("_______________________This is Error____________________")
                        errMsg = "____________File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
                        print("This is Azure errorMsg: ",errMsg) #new
                finally:
                   
                    await asyncio.sleep(10)

        self.bg_task = self.bot.loop.create_task(interval())
#[ReadTimeout] HTTPSConnectionPool(host='m.facebook.com', port=443): Read timed out. (read timeout=5) 應該是網路錯誤
        async def interval2():  
            await self.bot.wait_until_ready()  
            self.mumi = 0
            while not self.bot.is_closed():
                await asyncio.sleep(10) 
                try:
                    await asyncio.sleep(20)  
                    try_count = 0     
                    while True:  
                        try:                          #抓取 bh3TW粉絲團
                            article_list = get_posts('bh3TW', pages=2,cookies='cookie.json')  
                            await asyncio.sleep(15)
                            print("honkai_try_count = ",try_count)
                        except Exception as ex:
                            await asyncio.sleep(10) #爬蟲失敗 等待10秒
                            print("Exception happend",ex)
                            try_count +=1

                        else:
                            for bang in article_list: 
                                textall = f"{(bang['time']+datetime.timedelta(minutes=480)).strftime('%Y-%m-%d %H:%M:%S')}\n{ bang['text'][:800]}\n{ bang['post_url']}"

                                await asyncio.sleep(15)  # 冷卻秒 沒有BOT啟動不了 
                                
                                print("honkai outer mumi = ", self.mumi)
                                
                                if f"{bang['post_id']}" not in time_list("honkai_id"
                                ,"https://jsonstorage.net/api/items/2f56860a-6c3f-4f6a-b0fc-656751b9e027"
                                ,"2f56860a-6c3f-4f6a-b0fc-656751b9e027")[0] and self.counter < 3:
                                    self.honkai_channel = self.bot.get_channel(823235565473366030)#崩壞ID:823235565473366030
                                    await self.honkai_channel.send(textall)
                                    await asyncio.sleep(2)
                                    for image in bang['images']: #把images裡所有的圖一個一個列印出來
                                        await self.honkai_channel.send(f"\n{image}") 
                                        await asyncio.sleep(2) #放個CD避 免URL擠成一團
                                    self.mumi += 1
                                    print("honkai inside mumi = ", self.mumi)
                                    upd(f"{bang['post_id']}",f"{bang['time'].strftime('%H:%M:%S')}",
                                    'https://jsonstorage.net/api/items/2f56860a-6c3f-4f6a-b0fc-656751b9e027',
                                    "2f56860a-6c3f-4f6a-b0fc-656751b9e027","honkai") #新贈並上傳資料庫
                                    await asyncio.sleep(20)
                                elif self.mumi == 3:
                                    self.mumi = 0
                                                                  
                                    break   #mumi=3 跳出while true迴圈
                                else:
                                    self.mumi += 1
                                    await asyncio.sleep(10)

                            break
                    self.mumi = 0
                    tz = timezone(timedelta(hours=+8))
                    check_time = dt.now(tz).strftime('%H:%M:%S')  # 時間確認
                    print("honkai Now Time : ", check_time)  # 幹aws print 不能懂中文啦                      
                    print("honkai sleep   ( ✖ ︿ ✖ )")        
                    await asyncio.sleep(1800) #此循環 每1800秒執行一次
                                                 
                except Exception as e:
                        error_class = e.__class__.__name__ #取得錯誤類型
                        detail = e.args[0] #取得詳細內容
                        cl, exc, tb = sys.exc_info() #取得Call Stack
                        lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
                        fileName = lastCallStack[0] #取得發生的檔案名稱
                        lineNum = lastCallStack[1] #取得發生的行號
                        funcName = lastCallStack[2] #取得發生的函數名稱
                      #  print("_______________________This is Error____________________")
                        errMsg = "________File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
                        print("This is Honkai errorMsg: ",errMsg)
                finally:
                     await asyncio.sleep(5)

        self.bg_task = self.bot.loop.create_task(interval2())
         # json 規則 https://jenifers001d.github.io/2019/12/11/Python/learning-Python-day9/
         #json 寫入 https://www.geeksforgeeks.org/append-to-json-file-using-python/
        #try (嘗試做可能會失敗的事情)
        #except (失敗時要做甚麼)
        #else (成功時要做甚麼事情)
        #finally (不管成功還失敗，都要做的事情)

        async def interval3():      #新任務 彈射世界fb
            await self.bot.wait_until_ready() 
            self.wflipper = 0
            while not self.bot.is_closed():
                await asyncio.sleep(5) 
                try:
                    await asyncio.sleep(10)        
                    try_count = 0     
                    while True:  
                        try:        
                            article_list = get_posts('WorldFlipper.TW', pages=2,cookies='cookie.json')  
                            await asyncio.sleep(7)
                            print("wflipper_try_count = ",try_count)
                        except Exception as ex:
                            await asyncio.sleep(5) 
                            print("Exception happend",ex)
                            try_count +=1

                        else:
                            for wf_post in article_list: 
                                textall = f"{(wf_post['time']+datetime.timedelta(minutes=480)).strftime('%Y-%m-%d %H:%M:%S')}\n{ wf_post['text'][:800]}\n{ wf_post['post_url']}"

                                await asyncio.sleep(7)  
                               
                                print("wflipper outer  = ", self.wflipper)
                                
                                if f"{wf_post['post_id']}" not in time_list("wflipper_id"
                                ,"https://jsonstorage.net/api/items/ad6c7f02-2d32-4936-8fce-083775f407b8"
                                ,"ad6c7f02-2d32-4936-8fce-083775f407b8")[0] and self.counter < 3:
                                    self.honkai_channel = self.bot.get_channel(849689971987054663)
                                    await self.honkai_channel.send(textall)
                                    await asyncio.sleep(2)
                                    for image in wf_post['images']: 
                                        await self.honkai_channel.send(f"\n{image}") 
                                        await asyncio.sleep(2) 
                                    self.wflipper += 1
                                    print("wflipper inside = ", self.wflipper)
                                    upd(f"{wf_post['post_id']}",f"{wf_post['time'].strftime('%H:%M:%S')}",
                                    'https://jsonstorage.net/api/items/ad6c7f02-2d32-4936-8fce-083775f407b8',
                                    "ad6c7f02-2d32-4936-8fce-083775f407b8","wflipper") 
                                    await asyncio.sleep(10)
                                elif self.wflipper == 3:
                                    self.wflipper = 0
                                                                  
                                    break   
                                else:
                                    self.wflipper += 1
                                    await asyncio.sleep(5)

                            break
                    self.wflipper = 0
                    tz = timezone(timedelta(hours=+8))
                    check_time = dt.now(tz).strftime('%H:%M:%S') 
                    print("wflipper Now Time : ", check_time)                       
                    print("wflipper sleep  0.<")        
                    await asyncio.sleep(1800) #此循環 每1800秒執行一次
                                                 
                except Exception as e:
                        error_class = e.__class__.__name__ #取得錯誤類型
                        detail = e.args[0] #取得詳細內容
                        cl, exc, tb = sys.exc_info() #取得Call Stack
                        lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
                        fileName = lastCallStack[0] #取得發生的檔案名稱
                        lineNum = lastCallStack[1] #取得發生的行號
                        funcName = lastCallStack[2] #取得發生的函數名稱
                      #  print("_______________________This is Error____________________")
                        errMsg = "________File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
                        print("This is wflipper errorMsg: ",errMsg)
                finally:
                     await asyncio.sleep(3)

        self.bg_task = self.bot.loop.create_task(interval3())



        #非背景程式不要用 async def 會有↓
        #TypeError: 'coroutine' object is not subscriptable
        def res_append(scrap_id,scrap_datetime,address,ad_id,scrap_fb):
            response = requests.get(address,{"id":ad_id}) #新增value(疊加

            data = response.json()
            if scrap_fb == "azure":                     #寫入資料庫的格式
                content = {"azure_id":scrap_id,"azure_datetime":scrap_datetime}
            elif scrap_fb == "honkai":
                content = {"honkai_id":scrap_id,"honkai_datetime":scrap_datetime}
            elif scrap_fb == "wflipper":
                content = {"wflipper_id":scrap_id,"wflipper_datetime":scrap_datetime}
            else:
                pass
            data.append(content)
            return data

        def time_list(what_value,req_address,req_id): #將json裡的某個值放進list
            response = requests.get(req_address,{"id":req_id})
            data = response.json()
            time=[]
            for i in range(0,len(data)): #印出所有發文時間
                time.append(data[i][what_value])
            return time,data

        def upd(up_id,up_datetime,address,ad_id,scrap_fb):    #上傳至雲端json
            update = requests.put(address,
            params =   {"id":ad_id},
            json = res_append(up_id,up_datetime,address,ad_id,scrap_fb)
            )





    @commands.command()
    async def set_channel(self, ctx, ch: int):  # ch 頻道的參數 #設定定時發送文字在哪個頻道
        self.channel = self.bot.get_channel(ch)
        await ctx.send(f'Set Channel:{self.channel.mention}')  # .mation 提及

    @commands.command()
    async def set_time(self, ctx, time): #設定 定時發送的時間
       # self.counter = 0
        with open('setting.json', 'r', encoding='utf8') as jfile:
            jdata = json.load(jfile)
        await ctx.send("定時成功")

        jdata['time'] = time  # 使用者輸入的time傳入到jdata
        with open('setting.json', 'w', encoding='utf8') as jfile:  # w = 寫入
            json.dump(jdata, jfile, indent=4, ensure_ascii=False)  # indent 縮排

    


def setup(bot):
    bot.add_cog(Task(bot))



