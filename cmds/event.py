import discord
from discord.ext import commands
import json
from core.classes import Cog_Extension
import random
import json,asyncio
import datetime
from datetime import tzinfo, timedelta, datetime, timezone
from _datetime import date
import requests



with open('setting.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)


class ComplexEncoder(json.JSONEncoder):  #避免json紀錄亂碼
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

class Event(Cog_Extension):
   
    @commands.Cog.listener()
    async def on_member_join(self,member):
        channel = self.bot.get_channel(int(jdata['Welcome_channel']))
        await channel.send(F'{member} join!')

    @commands.Cog.listener()
    async def on_member_remove(self,member):
        channel = self.bot.get_channel(int(jdata['Leave_channel']))
        await channel.send(F'{member} join!')

    @commands.Cog.listener()
    async def on_message(self,msg):
        
        def server_info(n,n_value,what_value,req_address,req_id): #將json裡的某個值放進list
            response = requests.get(req_address,{"id":req_id})
            data = response.json()
            server=[]
            for i in range(0,len(data[n][n_value])):        #把資料庫紀錄的所有聊天室頻道放入list
                server.append(data[n][n_value][i][what_value])
            return server

        keyword2 = ['早安','早上好','morning','喔嗨唷'] #關鍵字list
        keyword3 = ['哈哈哈哈哈','哈哈哈哈','哈哈哈','哈哈哈哈哈哈']
        keyword4 = ['青椒','茄子']
        keyword5 = ['壽司','炸雞']
        keyword6 = ['滑倒','滑','地板','濕滑','痛','疼']
        keyword7 = ['一代一代一代','好痛']
        keyword8 = ['畝咪','畝瞇','拇咪','姆瞇','瞇','姆眯']
        userID =[268570448294445056,557103501256163348,396382675352682496, #限制使用者ID list
        570577760423247874,665477311855853587,492405187063971852,298036630533439489
        ,394885724652044288,111042061058236416,277108867131768834,264797041497079808
        ,290101369237667841,358745369020203019,268703413326446593,268701681926012928
        ,186009076839219202,197093567368265738,268795256013717506]
        # channel_ID = [750770142740348948,396383026533105685,665548661719171083,692774544858939393,
        # 700774634387275836,743370434048950272,849689971987054663,849662785930919986,847416153377603614]
        channel_ID = server_info(0,"channel_info","channel_id"
        ,"https://jsonstorage.net/api/items/0bb0a3f0-2274-4699-9834-4d9a9a027d19"
        ,"0bb0a3f0-2274-4699-9834-4d9a9a027d19") 
        #tz = timezone(timedelta(hours=+8))  
        now_time = datetime.now()#.strftime('%Y-%m-%d %H:%M:%S')
        #print(jdata['Lasttime'])
        #print(type(jdata['Lasttime']))
        lasttime = datetime.strptime(str(jdata['Lasttime']),'%Y-%m-%d %H:%M:%S')
        #print(now_time)
        #print('--------------')
        #print(lasttime)
        #print("now_time",type(now_time))
        #print("lasttime",type(lasttime))
        comparetime = (now_time - lasttime).seconds #比較上次與這次使用指令的時間 #製作出"使用冷卻時間"
        #print(comparetime)
        random_sp4 = random.choice(jdata['sp4'])
        ma = msg.author.id #純縮寫
        c_channel = msg.channel.id
            #以下為各種關鍵字觸發  # <:dragon2:811158756674895894> <-這個是 discord表情符號id
        if msg.content.startswith ('<:dragon2:811158756674895894>') and msg.author != self.bot.user:
            random_dragon2 = random.choice(jdata['dragon2'])        #!= self.bot.user 避免機器人回覆關鍵字 造成無限循環
            await msg.channel.send(random_dragon2) #傳送回話到該聊天頻道
        elif msg.content.startswith ('恐龍') and msg.author != self.bot.user and c_channel in channel_ID:
            await msg.channel.send('<:what:743821447528710194>') 
       # elif msg.content.startswith ('佬') and msg.author != self.bot.user and ca in channel_ID:
       #     await msg.channel.send('<:dragon1:697871931613118485>')
        elif '佬' in msg.content and msg.author != self.bot.user and c_channel in channel_ID:
            random_lao = random.choice(jdata['lao'])
            await msg.channel.send(random_lao)
        elif msg.content.startswith ('早') and msg.author != self.bot.user and ma in userID and c_channel in channel_ID: #keyword2
            await msg.channel.send(random_sp4)
        elif msg.content.endswith ('晨') and msg.author != self.bot.user and ma in userID and c_channel in channel_ID: #keyword2
            await msg.channel.send(random_sp4)
        elif msg.content in keyword2 and msg.author != self.bot.user and ma in userID and c_channel in channel_ID:  #keyword2
            await msg.channel.send(random_sp4)
        elif msg.content in keyword3 and msg.author != self.bot.user:   #keyword3
            await msg.channel.send('<:dragon7:700692124215279616>')
        elif msg.content.startswith ('皮蛋') and msg.author != self.bot.user and ma in userID and c_channel in channel_ID: #keyword4
            await msg.channel.send('<:no:744466544251109398>')
        elif msg.content.endswith ('皮蛋粥') and msg.author != self.bot.user and ma in userID and c_channel in channel_ID:#keyword4
            await msg.channel.send('<:no:744466544251109398>')
        elif msg.content in keyword4 and msg.author != self.bot.user and ma in userID and c_channel in channel_ID: #keyword4
            await msg.channel.send('<:no:744466544251109398>')
        elif msg.content.startswith ('洋芋片') and msg.author != self.bot.user and ma in userID and c_channel in channel_ID: #keyword5
            await msg.channel.send('<:yes:744466513939005440>')
        elif msg.content.endswith ('冰淇淋') and msg.author != self.bot.user and ma in userID and c_channel in channel_ID:#keyword5
            await msg.channel.send('<:yes:744466513939005440>')
        elif msg.content in keyword5 and msg.author != self.bot.user and ma in userID and c_channel in channel_ID: #keyword5
            await msg.channel.send('<:yes:744466513939005440>')
        elif '幹嘛' in msg.content and ma in userID and c_channel in channel_ID:
            await msg.channel.send(msg.author.name +' 沒禮貌')
        elif '好正' in msg.content and ma in userID and c_channel in channel_ID:
            await msg.channel.send(msg.author.mention +' 你好噁心')    #msg.author.mention 會tag 發言人 
        elif '呀呼' in msg.content:
            await msg.channel.send('<:Lan_NG:744550198210068523>')
        elif '你知道' in msg.content and ma in userID and c_channel in channel_ID:
            await msg.channel.send(msg.author.name +'  <:ik:744944189359521802>')
        elif msg.content.startswith ('窩不知道') and ma in userID and c_channel in channel_ID: 
            await msg.channel.send('<:idk:744944137639428147>')
        elif msg.content.startswith ('抽') and ma in userID and c_channel in channel_ID: 
            await msg.channel.send('https://cdn.discordapp.com/attachments/743370434048950272\
/744945561261834300/0b349375e040be5b3029a1a12b2da443_w48_h48.gif')
        elif msg.content.startswith ('<:dragon3:697876379340898365>') and msg.author != self.bot.user: 
            random_dragon3 = random.choice(jdata['dragon3'])
            await msg.channel.send(random_dragon3)
        elif '莎莉88.gif' in msg.content and msg.author != self.bot.user: 
            await msg.channel.send('https://media.discordapp.net/attachments/580782757798739993\
/618456010654351361/1563302229133.gif')
        elif '莎莉88.GIF' in msg.content and msg.author != self.bot.user: 
            await msg.channel.send('https://media.discordapp.net/attachments/580782757798739993\
/618456010654351361/1563302229133.gif')
        elif 'Mumibot' in msg.content and msg.author != self.bot.user and c_channel in channel_ID: 
            await msg.channel.send('https://media.discordapp.net/attachments/396383026533105685\
/725322147463036938/12e5bbf396f5aebc8da4fd65fbbc192c_w35_h25.gif')
        elif 'mumibot' in msg.content and msg.author != self.bot.user and c_channel in channel_ID: 
            await msg.channel.send('https://media.discordapp.net/attac\
hments/396383026533105685/725322147463036938/12e5bbf396f5aebc8da4fd65fbbc192c_w35_h25.gif')
        elif msg.content.startswith ('<:doragon2:701434320983687177>') and msg.author != self.bot.user: 
            await msg.channel.send('https://media.discordapp.net/attachments/396383026533105685\
/731786950259769395/c9406c3725b433f86b81a9ec76a22666_w48_h48.gif')
        elif msg.content.startswith ('你要') and msg.author \
            != self.bot.user and ma in userID and c_channel in channel_ID:
            await msg.channel.send('<:ALL:744955579595882537><:want:744955604610842676>')
        elif '我婆' in msg.content and ma in userID and c_channel in channel_ID:
            await msg.add_reaction("<:wake:745221468157116538>")
        elif '蝦' in msg.content and ma in userID and c_channel in channel_ID: 
            await msg.add_reaction("<:doge2:741336412091056218>")
        elif msg.content.startswith ('<:doragon3:701502829776601168>') and msg.author != self.bot.user:
            random_doragon3 = random.choice(jdata['doragon3'])
            await msg.channel.send(random_doragon3)
        elif '狗' in msg.content and ma in userID and c_channel in channel_ID:
            await msg.add_reaction("<:dog1:747691085702234173>")
            await msg.add_reaction("<:dog3:747691153427791872>")
            await msg.add_reaction("<:dog4:747691196050178058>")
            await msg.add_reaction("<:dog87:747691119927885826>")
        elif '火鍋' in msg.content and ma in userID and c_channel in channel_ID:
            random_hotpot = random.choice(jdata['hotpot'])
            await msg.channel.send(random_hotpot)
        elif msg.content in keyword6 and msg.author != self.bot.user and ma in userID and c_channel in channel_ID:
            random_wet = random.choice(jdata['wet'])
            await msg.channel.send(random_wet)
        elif msg.content in keyword7 and msg.author != self.bot.user and ma in userID and c_channel in channel_ID:
            random_edai = random.choice(jdata['edai'])
            await msg.channel.send(random_edai)
        elif 'peko' in msg.content and msg.author != self.bot.user and ma in userID and c_channel in channel_ID:
            random_wet = random.choice(jdata['wet'])
            await msg.channel.send(random_wet)
        elif 'PEKO' in msg.content and msg.author != self.bot.user and ma in userID and c_channel in channel_ID:
            random_wet = random.choice(jdata['wet'])
            await msg.channel.send(random_wet)
        elif '好油喔' in msg.content and msg.author != self.bot.user and ma in userID and c_channel in channel_ID:
            random_wet = random.choice(jdata['wet'])
            await msg.channel.send(random_wet)
        elif '好油ㄛ' in msg.content and msg.author != self.bot.user and ma in userID and c_channel in channel_ID:
            random_wet = random.choice(jdata['wet'])
            await msg.channel.send(random_wet)
        elif '姆咪' in msg.content and msg.author != self.bot.user and ma in userID and c_channel in channel_ID:
            random_mumi = random.choice(jdata['mumi'])
            await msg.channel.send(random_mumi)
        elif msg.content in keyword8 and msg.author != self.bot.user and ma in userID and c_channel in channel_ID:
            await msg.channel.send('姆咪<:doge2:741336412091056218><:dog1:747691085702234173><:dog3:747691153427791872>\
<:dog4:747691196050178058><:dog87:747691119927885826> ')
        elif 'ㄍㄧ' in msg.content and ma in userID and c_channel in channel_ID and comparetime > 10:
            random_roger = random.choice(jdata['roger'])        #此指令有冷卻時間，使用指令後把當前時間寫入json
            now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            jdata['Lasttime'] = now_time
            
            with open('setting.json','w',encoding='utf8') as jfile:  
                json.dump(jdata,jfile,indent=4,cls=ComplexEncoder,ensure_ascii=False)
            await msg.channel.send(random_roger)
        elif '結束' in msg.content and msg.author != self.bot.user and ma in userID and c_channel in channel_ID:
            random_over = random.choice(jdata['over'])
            await msg.channel.send(random_over)
        elif "@!268570448294445056" in msg.content and msg.author != self.bot.user and c_channel in channel_ID:
            random_mumi_mention = random.choice(jdata['mumi_mention'])
            await msg.channel.send(random_mumi_mention)
        elif "@!743339674143031298" in msg.content and msg.author != self.bot.user and c_channel in channel_ID:
            random_dragon_mention = random.choice(jdata['dragon_mention'])
            await msg.channel.send(random_dragon_mention)
        elif "!SOP" in msg.content and msg.author != self.bot.user and ma in userID and c_channel in channel_ID:
            await msg.channel.send("<:819165653927329823:828298199089283072> <:819165653927329823:828298199089283072>")
        elif "!sop" in msg.content and msg.author != self.bot.user and ma in userID and c_channel in channel_ID:
            await msg.channel.send("<:no:744466544251109398><:no:744466544251109398> $sop<:yes:744466513939005440>")
        elif "!一代一代一代" in msg.content and msg.author != self.bot.user and ma in userID and c_channel in channel_ID:
            await msg.channel.send("以待不用驚嘆號啦 <:819165653927329823:828298199089283072>")

    # server_info(0,"channel_info","channel_id"
    # ,"https://jsonstorage.net/api/items/0bb0a3f0-2274-4699-9834-4d9a9a027d19"
    # ,"0bb0a3f0-2274-4699-9834-4d9a9a027d19")

#cmd中  cd pic = 進到pic資料夾
#dir=列出目前在的資料夾中 所有的文件

#4/8 2點到8點 停止運行  

#看LOG heroku logs --tail

# 2021-04-08T05:34:08.443520+00:00 heroku[worker.1]: Error R12 (Exit timeout) -> At least one process failed to exit within 30 seconds of SIGTERM
# 2021-04-08T05:34:08.447254+00:00 heroku[worker.1]: Stopping remaining processes with SIGKILL
# 2021-04-08T05:34:08.569959+00:00 heroku[worker.1]: Process exited with status 137
# 2021-04-08T05:34:25.014474+00:00 app[worker.1]: honkai_try_count =  0

        

def setup(bot):
    bot.add_cog(Event(bot))

