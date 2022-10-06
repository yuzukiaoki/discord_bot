from asyncio.tasks import sleep
import discord
from discord import player
from discord.ext import commands
import json
from core.classes import Cog_Extension
import random
import json,asyncio
import datetime
from datetime import tzinfo, timedelta, datetime, timezone
#from datetime import date #原本 from _datetime import date
import requests
from data_file.get_something import *
from functools import partial



with open('mumi_setting.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        # elif isinstance(obj, date):
        #     return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

class Event(Cog_Extension):


    def __init__(self, *args, **kwargs):  # 基本化自訂函式
        super().__init__(*args, **kwargs)

        self.image_types = ["png", "jpeg", "gif", "jpg","webp","bmp"]

        self.local_time = set_timeznoe(8).strftime('%Y-%m-%d')
        self.upload_tasks = [] # 任務欄位
        self.sleep_time = 1800  # 考慮任務頻率每30分鐘一次
        self.bot.loop.create_task(self.background_task())  # 我希望每分鐘，就檢查一次，有沒有任務清單要處理

    @commands.Cog.listener()
    async def on_message(self,msg): 
        await self.replyBot(msg)
        get__channel = self.bot.get_channel(9329101467093514267016)# 很讚圖庫
        get_great_channel = self.bot.get_channel(9335679414388072360370) #好耶圖庫
        channel_list = [get__channel.id,get_great_channel.id]
        have_img = False
        if msg.channel.id in channel_list and msg.author != self.bot.user: #特定頻道抓取反應
            for attachment in msg.attachments:
                if any(attachment.filename.lower().endswith(image) for image in self.image_types):  # 當我收到訊息，先檢查是否有檔案，有檔案我就增加儲存圖片的任務
                    have_img = True #只要該"次"訊息含有圖片，則跳脫迴圈
                    break

            if have_img:  #確認該次訊息含有圖片，執行加圖片任務
                self.upload_tasks.append(partial(self.image_task, msg))  # 增加任務
        else:
            pass

    async def background_task(self):  # 重複執行的腳本
        try:
            await self.bot.wait_until_ready()
            channel = self.bot.get_channel(940115771925177655326) #任務回報 頻道
 
            while not self.bot.is_closed():
                local_time = set_timeznoe(8).strftime('%m-%d %H:%M') # 任務執行完畢後 顯示當前時間
                await channel.send(f"總共有{len(self.upload_tasks)}個任務，Ready to do <:474209241654362122:811230849927479366>")
                for task in self.upload_tasks:
                    
                    result = await task()  # 從任務列表中，取出任務並且執行(這裡的task只是被partial包裝了，實際上執行的就是image_task)
                    # if result:
                    #     await channel.send(f"任務執行成功，還剩餘{len(self.upload_tasks)}個任務")
                    # else:
                    #     await channel.send("任務失敗，請檢查")
                #await channel.send(f"任務執行完畢，完成{len(self.upload_tasks)}個任務")
                self.upload_tasks = []
                await channel.send(f"{local_time} 任務執行成功")
                #print("睡了吧?")
                await asyncio.sleep(self.sleep_time)  # 休息，避免執行太頻繁

        except Exception as ex:
            print("tasks loop error:\n", ex)

    async def image_task(self, message):
        # 我的任務要做兩件事情
        # 執行上傳api，並且回傳成功或失敗的訊息
        result = await self.getImgUrl(message)
        return result

    async def replyBot(self,msg):

        self.userID =get_server(
        "https://api.jsonstorage.net/v1/json/cc3a38bc-d03a-43bd-b2dc-0d41270434cf1/17661465-b197-4dd4-a989-e3ffd4ce4d69?apiKey=" #mix_json
         ,"17661465-b197-4dd4-a989-e3ffd4ce4d69?apiKey=","bot_user","bot_user_id")
        self.channel_ID = some_list("channel_id"
        ,"https://api.jsonstorage.net/v1/json/cc3a38bc-d03a-43bd-b2dc-0d41127034cf1/17661465-b197-4dd4-a989-e3ffd4ce4d69?apiKey=" #mix_json
        ,"17661465-b197-4dd4-a989-e3ffd4ce4d69?apiKey=",1,"channel_info")
        now_time = set_timeznoe(8)#.strftime('%Y-%m-%d %H:%M:%S')
        lasttime = datetime.strptime(str(jdata['Lasttime']),'%Y-%m-%d %H:%M:%S')
        comparetime = (now_time - lasttime).seconds
        ma = msg.author.id
        c_channel = msg.channel.id

        check_map = { # 把關鍵字整理成一個map
        "測試範本":{ # 為這組關鍵字取個一名字，類似取function名，隨便都行
            "trigger":["測試測試測試"], # 要觸發的關鍵字 list
            "action": lambda: msg.channel.send("==")# 觸發時要做的行動，別管lambda是啥，反正丟在lambda後面就對了，可以丟define
        },
        "shi":{ #另一組
            "trigger":["sao","starburst"],
            "action":lambda: msg.channel.send("==?")
        },
        "大佬":{ 
            "trigger":["佬"],
            "action":lambda: mix_reaction(msg,5,10,15,'lao','n')
        },
        "dragon2":{ 
            "trigger":["<:dragon2:811158756674895894>"],
            "action":lambda: random_react('dragon2',msg)
        },
        "嫩":{ 
            "trigger":["嫩"],
            "action":lambda: mix_reaction(msg,50,60,20,'sp4','n') #,'n'
        },
        "噓":{ 
            "trigger":['噓噓噓噓噓','噓噓噓噓','噓噓噓','噓噓噓噓噓噓'],
            "action":lambda: msg.channel.send("<:dragon7:700692124215279616>")
        },
        "你知道":{ 
            "trigger":["你知道","妳知道"],
            "action":lambda: mix_reaction(msg,60,70,3,"msg",'<:idk:744944137639428147>')
        },
        "窩不知道":{ 
            "trigger":["窩不知道","我不知道"],
            "action":lambda: mix_reaction(msg,50,60,10,"msg",msg.author.name +'  我知道<:dragon6:698619245143130193>')
        },
        "抽":{ 
            "trigger":["抽"],
            "action":lambda: mix_reaction(msg,5,10,5,'draw','n')
        },
        "dragon3":{ 
            "trigger":["<:dragon3:697876379340898365>"],
            "action":lambda: mix_reaction(msg,40,50,5,'dragon3','n')
        },
        "沙礫88":{ 
            "trigger":["莎莉88.gif","砂礫88.gif","沙粒88.gif","沙礫88.gif"],
            "action":lambda: msg.channel.send('https://media.discordapp.net/attachments/580782757798739993\
/618456010654351361/1563302229133.gif')
        },
        "手套襪子":{ 
            "trigger":["mumibot","手套襪子","恐龍"],
            "action":lambda: msg.channel.send('https://media.discordapp.net/attachments/708892923420213288\
/713377203894747156/1069461.gif')
        },
        "doragon2":{ 
            "trigger":["<:doragon2:701434320983687177>"],
            "action":lambda: mix_reaction(msg,40,50,5,"msg",'https://media.discordapp.net/attachments/396383026533105685\
/731786950259769395/c9406c3725b433f86b81a9ec76a22666_w48_h48.gif')
        },
        "你要":{ 
            "trigger":["你要","妳要"],
            "action":lambda: mix_reaction(msg,10,30,6,"msg",'<:ALL:744955579595882537><:want:744955604610842676>')
        },
        "狗":{ 
            "trigger":["狗"],
            "action":lambda: add_all_reaction(msg,40,50,"<:dog1:747691085702234173>","<:dog3:747691153427791872>"
            ,"<:dog4:747691196050178058>","<:dog87:747691119927885826>")
        },
        "三小":{ 
            "trigger":["三小"],
            "action":lambda: add_all_reaction(msg,40,50,"<:doge2:741336412091056218>")
        },
        "doragon3":{ 
            "trigger":["<:doragon3:701502829776601168>"],
            "action":lambda: mix_reaction(msg,60,70,3,'doragon3','n')
        },
        "火鍋":{ 
            "trigger":["火鍋","hotpot"],
            "action":lambda: mix_reaction(msg,90,100,5,'hotpot','n')
        },
        "滑倒":{ 
            "trigger":['滑倒','好油ㄛ','好油喔'],
            "action":lambda: mix_reaction(msg,40,50,10,'wet','n')
        },
        "一代一代":{ 
            "trigger":['一代一代一代','以待以待以待','一代一代'],
            "action":lambda: random_react('edai',msg)
        },
        "姆咪":{ 
            "trigger":["姆咪"],
            "action":lambda: mix_reaction(msg,70,80,10,'mumi','n')
        },
        "結束":{ 
            "trigger":["結束","一切都"],
            "action":lambda: mix_reaction(msg,30,40,16,'over','n')
        },
        "tag_mumi":{ 
            "trigger":["<@268570448294445056>"],#@!268570448294445056 此寫法已失效
            "action":lambda: random_react('mumi_mention',msg)
        },
        "tag_dragon":{ 
            "trigger":["<@743339674143031298>"],
            "action":lambda: random_react('dragon_mention',msg)
        },
        "87":{ 
            "trigger":["!一代一代一代"],
            "action":lambda: msg.channel.send("幹 以待不用驚嘆號啦幹 <:819165653927329823:828298199089283072>")
        },
        "特別觸發":{ 
            "trigger":["這裡好像有甚麼都不重要"],
            "action":lambda: mix_reaction(msg,10,11,30,'vt',"react","<:wet:811109729727545364>")
        }
        
        # "狗":{ 
        #     "trigger":["狗"],
        #     "action":lambda: add_all_reaction()
        # }
                    }
        otherWord = ["http"] #不知道為甚麼不能用這個?
        trigger_count = 0 # 記錄觸發次數，避免一句話如果 sao 跟 peko 同時存在，會回復兩次訊息
        if msg.author != self.bot.user and ma in self.userID and c_channel in self.channel_ID:
            for key in check_map:
                if trigger_count > 0: # 有記錄代表有觸發過，就別執行了
                    break

                key_words = check_map[key].get("trigger",[])
                for word in key_words:
                    if "http" in msg.content and "holodex" in msg.content:
                        await check_map["特別觸發"]["action"]()
                        trigger_count +=1
                        break 
                    elif word in msg.content:
                        await check_map[key]["action"]()
                        trigger_count += 1 # 有觸發就加1
                        break # 如果已經找到同組的關鍵字，就不用再找了

                    elif word.upper() in msg.content:  #確認小寫轉大寫
                        await check_map[key]["action"]()
                        trigger_count += 1 
                        break

                    elif word.title() in msg.content:  #確認開頭大寫
                        await check_map[key]["action"]()
                        trigger_count += 1 
                        break 
        else:
            pass

        #在外層先包一層　msg.author != self.bot.user and ma in user ID and c_channel in channel_id
        if msg.content.startswith ('恐龍88') and msg.author != self.bot.user:
            random_dragon2 = random.choice(jdata['dragon2'])
            await msg.channel.send(random_dragon2)
        elif msg.content.startswith ('繃繃跳') and msg.author != self.bot.user and c_channel in self.channel_ID: # wait_for的應用 暫時想不到能幹嘛
            channel = msg.channel
            await channel.send('Send me that 👍 reaction, mate')

            def check(reaction, user):
                return user == msg.author and str(reaction.emoji) == '👍'

            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await channel.send('👎')
            else:
                await channel.send('👍')
        elif "!SOP" in msg.content and msg.author != self.bot.user and ma in self.userID and c_channel in self.channel_ID:
            await msg.channel.send("<:819165653927329823:828298199089283072> <:819165653927329823:828298199089283072>")
        elif "!sop" in msg.content and msg.author != self.bot.user and ma in self.userID and c_channel in self.channel_ID:
            await msg.channel.send("<:no:744466544251109398><:no:744466544251109398> $sop<:yes:744466513939005440>")
        elif 'ㄍㄧ' in msg.content and ma in self.userID and c_channel in self.channel_ID and comparetime > 10:
            random_roger = random.choice(jdata['roger'])
            now_time = set_timeznoe(8).strftime('%Y-%m-%d %H:%M:%S')
            jdata['Lasttime'] = now_time
            
            with open('mumi_setting.json','w',encoding='utf8') as jfile:
                json.dump(jdata,jfile,indent=4,cls=ComplexEncoder,ensure_ascii=False)
            await msg.channel.send(random_roger)

        if msg.reference and msg.author.id != self.bot.user and ma in self.userID and c_channel in self.channel_ID: #只要有任何reply 這個 reference就會被觸發
            first_msg = msg # 最初的msg存入另一個變數
            msg = await msg.channel.fetch_message(msg.reference.message_id)
            if msg.author.id == 7433396414741413031298:
                if "知道" in first_msg.content and first_msg.author != self.bot.user : #還想玩我才不知道阿
                    # print("got it")
                    await asyncio.sleep(5)
                    await first_msg.reply("<:ik:744944189359521802>", mention_author=True)
                else:
                    random_reply_dragon = random.choice(jdata['dragon_reply']) #有人回覆恐龍訊息時觸發
                    await asyncio.sleep(5)
                    await first_msg.reply(random_reply_dragon, mention_author=False)
    # --------------------------------------------------
    async def getImgUrl(self,msg):
            get__channel = self.bot.get_channel(9329114067093515726016)# 很讚圖庫
            get_great_channel = self.bot.get_channel(93356793885702360370) #好耶圖庫

            pic_count = 0
            #file_count = 0 #讓 SPOILER_ 檔名不會一直重複
            if msg.channel.id == get__channel.id and msg.author != self.bot.user: #特定頻道抓取反應
                for attachment in msg.attachments:
                    if any(attachment.filename.lower().endswith(image) for image in self.image_types):
                       # await attachment.save(attachment.filename)
                        pic_count+=1
                        file = msg.attachments[pic_count-1] #多個attachments 利用pic_count的數字 推播出相應的attachment
                        #msg.attachments type為 'discord.message.Attachment'     #msg.attachments 是一個list
                        #if file_count == 0 :
                        file.filename = f"SPOILER_{file.filename}"
                        #file_count += 1 #只讓上面那個變數 在"迴圈內" 被賦予一次值 
                        spoiler = await file.to_file()
                        #色色頻道
                        
                        alltext = f"第 {pic_count} 張圖片<:683720686594031617:828301437477453914>\n\
                                    ID：{attachment.id}\n\
                                    size：{round(transfer_MB(attachment.size),4)} MB\n\
                                    width：{attachment.width}\n\
                                    height：{attachment.height}\n\
                                    檔案類型：{attachment.content_type}\n\
                                    上傳時間：{self.local_time}".replace(" ","") # 去除空格
                        await get__channel.send(alltext)
                        await asyncio.sleep(random_sleep(2,5))
                        await get__channel.send(file=spoiler)
                        await asyncio.sleep(random_sleep(2,5))
                        #await get_h_channel.send(f"url: {attachment.url}") # 記錄到DB
                        discord_upd("https://api.jsonstorage.net/v1/json/cc3a38bc-d03a-43bd-b2dc-0d4127034cf1/9c265be9-ce5f-45f8-bcd4-d55f378c3c29?apiKey=",
                        "9c265be9-ce5f-45f8-bcd4-d55f378c3c29?apiKey=",0,"download_url",0,
                        url = attachment.url, datetime = self.local_time, unicode = attachment.id, type = attachment.content_type)
                #await msg.delete()
            elif msg.channel.id == get_great_channel.id and msg.author != self.bot.user:
                for attachment in msg.attachments:
                    if any(attachment.filename.lower().endswith(image) for image in self.image_types):
                       # await attachment.save(attachment.filename)
                        # 普通頻道
                        pic_count+=1
                        alltext = f"第 {pic_count} 張圖片<:683720686594031617:828301437477453914>\n\
                                    ID：{attachment.id}\n\
                                    size：{round(transfer_MB(attachment.size),4)} MB\n\
                                    width：{attachment.width}\n\
                                    height：{attachment.height}\n\
                                    檔案類型：{attachment.content_type}\n\
                                    上傳時間：{self.local_time}".replace(" ","") # 去除空格
                        await get_great_channel.send(alltext)
                        await asyncio.sleep(random_sleep(2,5))
                        await get_great_channel.send(f"url: {attachment.url}") # 記錄到DB
                        await asyncio.sleep(random_sleep(2,5))
                        discord_upd("https://api.jsonstorage.net/v1/json/cc3a38bc-d03a-43bd-b2dc-0d4127034cf1/2b578e47-224e-490a-ab43-e2611780362b?apiKey=",
                        "2b578e47-224e-490a-ab43-e2611780362b?apiKey=",0,"normal_download_url",0,
                        n_url = attachment.url, n_datetime = self.local_time, n_unicode = attachment.id, n_type = attachment.content_type)
                #await msg.delete() 不能把圖刪掉 url會bang不見
            else:
                pass

            return True  #?_?


    @commands.Cog.listener()
    async def on_message_edit(self,before, after): 
        """
        可以觀看別人編輯前的文字 和編輯後的文字
        """
        if not before.author.bot:
            
            if 'http' not in before.content:
                self.edit_message_channel = self.bot.get_channel(913700174178266034196)
                # await self.edit_message_channel.send(
                #     f'{before.author} edit a message \n'
                #     f'Guild: {before.guild.name} \n'
                #     f'channel: {before.channel.name} \n'
                #     f'Before: {before.content}\n'
                #     f'After: {after.content}\n'
                #     '-----------------------------'     
                # )
                embed = discord.Embed(
                title = f"{before.author} edit a message",
                color = 9098044
                )
                embed.add_field(
                    name = "Guild",
                    value = f"{before.guild.name}",
                    inline = False
                )
                embed.add_field(
                    name = "channel",
                    value = f"{before.channel.name}",
                    inline = False
                )
                embed.add_field(
                    name = "Before",
                    value = f"{before.content}",
                    inline = False
                )
                embed.add_field(
                    name = "After",
                    value = f"{after.content}",
                    inline = False
                )
            

                await self.edit_message_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        """
        針對某個訊息的某個表情做反應
        """
        if reaction.emoji == "❓" and user != self.bot.user and user.id in self.userID and reaction.message.channel.id in self.channel_ID:
            if random_sleep(1,100) < random_sleep(50,60): #49%~59%機率觸發
                await reaction.message.add_reaction("❓")
                if random_sleep(1,100) < random_sleep(20,30): #19%~29%機率觸發
                    await reaction.message.add_reaction("🔫")
        #await reaction.message.channel.send(f"{user} reacted with {reaction.emoji}") #當有人按表情時，bot會說是誰按了表情

    @commands.Cog.listener()
    async def on_raw_message_delete(self,msg):
        """
        偵測頻道的 "刪除"事件(批次刪除不適用 機器人的批次刪除不適用)
        當被刪除的信息 並不保存在"緩存"中 ，則訊息物件 只會回傳None
        刪除Embed的話 會跑出 HTTP 400 bad request錯誤
        """
        del_msg_channel = self.bot.get_channel(1023826299694878780)#刪除文字log
        
        if msg.cached_message == None:
            embed = discord.Embed(
                title = "訊息刪除事件(無緩存)",
                color = 5665879
            )
            embed.add_field(
                name = "伺服器",
                value = f"{msg.guild_id}",
                inline = False
            )
            embed.add_field(
                name = "頻道",
                value = f"<#{msg.channel_id}>",
                inline = False
            )
            embed.add_field(
                name = "訊息ID",
                value = f"{msg.message_id}",
                inline = False
            )
            

            await del_msg_channel.send(embed=embed)
            # await del_msg_channel.send("抓不到緩存\n"
            #                           f"伺服器: {msg.guild_id}\n"
            #                           f"頻道: <#{msg.channel_id}>\n"
            #                           f"訊息ID: {msg.message_id}\n"
            #                           f"=================")
        else:
            embed = discord.Embed(
                title = "訊息刪除事件",
                color = 16746484
            )
            embed.add_field(
                name = "伺服器",
                value = f"{msg.guild_id}",
                inline = False
            )
            embed.add_field(
                name = "頻道",
                value = f"<#{msg.channel_id}>",
                inline = False
            )
            embed.add_field(
                name = "訊息ID",
                value = f"{msg.message_id}",
                inline = False
            )
            embed.add_field(
                name = "訊息作者",
                value = f"{msg.cached_message.author}",
                inline = False
            )
            embed.add_field(
                name = "訊息內容",
                value = f"{msg.cached_message.content}",
                inline = False
            )
            embed.add_field(
                name = "訊息圖片",
                value = f"{msg.cached_message.attachments}",
                inline = False
            )
            

            await del_msg_channel.send(embed=embed)




def setup(bot):
    bot.add_cog(Event(bot))