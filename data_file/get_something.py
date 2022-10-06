import requests ,random,discord
import sys,traceback,json,asyncio
from datetime import datetime as dt
from datetime import timedelta, timezone
from imgurpython import ImgurClient
from facebook_scraper import get_posts, exceptions

async def scrape_interval(bot, channel, fb_url, imgur, req_address, req_id ,get_key, scrape_fb, title="Facebook"): 
    """
    :param bot        => self.bot
    :param channel    => 機器人要推播到哪個頻道
    :param fb_url     => 要抓取的粉絲團網頁碼
    :param imgur      => imgur 私人相簿ID
    :param req_address=> api網址
    :param req_id     => api id
    :param get_key    => 想要變成一坨List的 key
    :param scrape_fb  => 抓取的FB，對應到 res_append()的條件
    :param title      => embed放置的標題
    """

    await bot.wait_until_ready() 
    erro_count = 0
    scrape_counter = 0
    scrape_temporary_banned_count = 0
    scrape_channel = bot.get_channel(channel)#崩壞ID:823235565473366030
    print(f"「{scrape_fb}」 interval Strat to sleep")

    start_cool = 600
    if scrape_fb == 'honkai':
        start_cool = start_cool *1
    elif scrape_fb == 'maple':
        start_cool = start_cool *2
    elif scrape_fb == 'azure':
        start_cool = start_cool *3
    else:
        print(f"{scrape_fb} 不在清單上")
        start_cool = start_cool * 3
    await asyncio.sleep(random_sleep(start_cool, start_cool+100)) # 起始先睡  若遇到 heroku循環不馬上抓資料 而是先睡
    while not bot.is_closed():
        await asyncio.sleep(random_sleep(10,60)) 
        try:
            await asyncio.sleep(random_sleep(10,60))     
            while True:  
                try:
                    # 獲取資訊在這裡
                    article_list = get_posts(fb_url, pages=2, cookies='cookie2.json')  # 得到文章列表
                    await asyncio.sleep(random_sleep(10,20))

                except exceptions.TemporarilyBanned as e:
                    
                    await asyncio.sleep(BannedError(scrape_temporary_banned_count,f"「{scrape_fb}」 Temporarily banned, sleeping for" ))
                    scrape_temporary_banned_count +=1 # 上面每執行一次多睡600秒

                else:
                    if article_list is not None:
                        for data in article_list: 
                            #textall = f"{(data['time'] + timedelta(minutes=480)).strftime('%Y-%m-%d %H:%M:%S')}\n{ data['text'][:800]}\n{ data['post_url']}"

                            await asyncio.sleep(random_sleep(10,15))  # 冷卻一秒 沒有BOT啟動不了 
                       
                            print(f"「{scrape_fb}」 outer mumi = ", scrape_counter)
                            
                            if f"{data['post_id']}" not in some_list(get_key, req_address, req_id, 0) and scrape_counter < 3:
 
                                await asyncio.sleep(2)
                                print(data['images'])
                                imgurList = []
                                if data['images'] is not None: #有時候  data['images'] 會是None
                                    
                                    for image in data['images']: #把images裡所有的圖一個一個列印出來
                                        
                                        for frequency in range(0,3): #當上傳失敗(可能遇到網路問題) 則印出錯誤，並且最多嘗試上傳三次，否則略過po圖
                                            try:
                                                await asyncio.sleep(frequency*10+1) #上傳失敗的冷卻
                                                #await asyncio.sleep(3) #有時候imgur圖片不會被預覽出來，放個延遲試試
                                                scrape_img = upload_photo(image, imgur)
                                                await asyncio.sleep(5)
                                  
                                                # print(f"「{scrape_fb}」 send to channel{scrape_channel}、channel {channel}") #驗證頻道
                                                imgurList.append(scrape_img)
                                                #await scrape_channel.send(f"\n{scrape_img}") #new one #imgur URL
                                                
                                            except Exception as ex:
                                                print(f"「{scrape_fb}」 upload image something wrong happened ＝ ＝") 
                                                print(ex)
                                                if frequency == 2:
                                                    print("upload Fail")
                                            else:
                                                break
                                            finally:
                                                await asyncio.sleep(2)
                                        #await honkai_channel.send(f"\n{image}") 
                                        await asyncio.sleep(2) #放個CD避 免URL擠成一團

                                color_list = [5132023,60090,9224447,8519935,14900735,16771328] #隨機邊框顏色
                                scrape_embed = discord.Embed(
                                        color = random.choice(color_list), 
                                        description = f"{data['text'][:800]}"
                                )
                                scrape_embed.set_author(name=title, url=f"{ data['post_url']}", icon_url="https://cdn.discordapp.com/attachments/672378454755550134276/1024197625005735947/98650216_p0_master1200.jpg" )
                                scrape_embed.set_footer(text=f"Send Time • {(data['time'] + timedelta(minutes=480)).strftime('%Y-%m-%d %H:%M:%S')}", 
                                                        icon_url="https://cdn.discordapp.com/attachments/845498766554431538/8454984445824520499241/ver.png")
                                if imgurList != []:
                                    scrape_embed.set_image(url=imgurList[0])
                                    if len(imgurList) > 1:
                                        await scrape_channel.send(embed=scrape_embed)
                                        for imgurImage in imgurList[1:]:
                                            await asyncio.sleep(3)
                                            await scrape_channel.send(imgurImage)

                                    else:
                                        await scrape_channel.send(embed=scrape_embed)    
                                    
                                else:
                                    await scrape_channel.send(embed=scrape_embed)


                                scrape_counter += 1
                                print(f"「{scrape_fb}」 ========inside mumi = ", scrape_counter)

                                upd(f"{data['post_id']}",f"{(data['time'] + timedelta(minutes=480)).strftime('%Y-%m-%d %H:%M:%S')}", req_address, req_id, scrape_fb) #新增並上傳資料庫
                                await asyncio.sleep(20)
                                
                            elif scrape_counter == 3:
                                scrape_counter = 0
                                                            
                                break   #mumi=3 跳出while true迴圈
                            else:
                                scrape_counter += 1
                                await asyncio.sleep(10)

                        break
                    else:
                        break
            scrape_counter = 0
            check_time = set_timeznoe(8).strftime('%H:%M:%S')
            print(f"「{scrape_fb}」 Now Time : ", check_time)  # 幹aws print 不能懂中文啦                      
            print(f"「{scrape_fb}」 Zzzzz....( ´ ▽ ` )ﾉ")        
            await asyncio.sleep(start_cool*3) #跳出迴圈 即進入冷卻
                                            
        except Exception as e:

            error_channel = bot.get_channel(1014378434782306304) # 錯誤回報頻道
            erro_count +=1 
            printError(e,f"This is 「{scrape_fb}」 errorMsg: ")
            print(f"Error Count : {erro_count}")
            if erro_count %3 ==0:
                print("The number of errors has reached three，a warning will be sent to Disocrd")
                await error_channel.send("<@268570448294445056>"+f" 「{scrape_fb}」 scrape錯誤失敗次數已達{erro_count}次")
                print("must go sleep for 12hours")
                await asyncio.sleep(12*3600)
                # print(f"Ready to sleep, sleep time {start_cool*3 + erro_count*100} sec")
                # await asyncio.sleep(start_cool*3 + erro_count*100)
                
        finally:
            await asyncio.sleep(random_sleep(10, 20))


async def em(channel):
    """
    1
    """
    n_download_url = "https://api.jsonstorage.net/v1/json/cc3a38bc-d03a-43bd-b2dc-0d4127034cf1/2b578e47-224e-490a-ab43-e2611780362b?apiKey="
    n_download_url_id ="2b578e47-224e-490a-ab43-e2611780362b?apiKey="

    with open('mumi_setting.json','r',encoding='utf8') as jfile:
        jdata = json.load(jfile)

    color_list = [0x92c256,0x9256c2,0x5692C2,0x56C292,0xC29256,0xC25692] #隨機邊框顏色

    embed=discord.Embed(
        title="你今天過得好嗎", 
        url=random.choice(jdata['surprise']), 
        color=random.choice(color_list), 
        timestamp= dt.now(timezone.utc)) #原為datetime.datetime.now() / 更該後可顯示當前時區
    embed.set_author(name="色圖哈囉", url=random.choice(some_list("n_url",n_download_url,n_download_url_id,1,"normal_download_url")),  #隨機好圖
                        icon_url="https://media.discordapp.net/attachments/708892923420213288/7133772038947444147156/1069461.gif")
    embed.set_thumbnail(url=random.choice(jdata['bird'])) #嵌入框又上的圖片

    embed.add_field(name="↑↗↘↙↑↗↘↙ click anything ↑↗↘↙↑↗↘↙↑", #嵌入框內容
                    value=random.choice(jdata['soldier']),
                    inline=True)

    await channel.send(embed=embed)


def transfer_MB(byte_thing):
    """
    將byte轉成MB
    """
    divisor = 1024 #divisor 除數
    transferKB = byte_thing/divisor
    transferMB = transferKB/divisor
    return transferMB


async def mix_reaction(msg,*args): #[random1, random2, sleeptime, msg or json, react or msg content, reaction]
    """
    混合的reaction 不只案表情也可以延遲指定時間並發送言論
    可以只要隨機發送json的value或是指定的文字，或是除了前面再加上表情符號，可以全功能都要
    """
    if random.randint(1,100) < random.randint(args[0],args[1]): #應該是 "<" 才對 右邊機率大於左邊
        if args[4] == "react":
            await msg.add_reaction(args[5])#"<:wet:811109729727545364>"
        else:
            pass
        await asyncio.sleep(args[2])
        if args[3] == "msg":
            await msg.channel.send(args[4],reference = msg , mention_author = False)
            pass
        elif args[3]:
            await random_react(args[3],msg)
        else:
            pass
    else:
        pass


async def add_all_reaction(msg,*args): #[random1, random2]
    """
    根據函數帶入的參數(args)數量，bot會增加幾個reaction，最多5個，
    """
    if random.randint(1,100) < random.randint(args[0],args[1]):
        if len(args)>2 :  #如果args這個list長度大於2 就推第2個表情 下面以此類推
            await msg.add_reaction(args[2])
        if len(args)>3 :
            await msg.add_reaction(args[3])
        if len(args)>4 :
            await msg.add_reaction(args[4])
        if len(args)>5 :
            await msg.add_reaction(args[5])
    else:
        pass

def random_react(json_document,msg): #random choice json 統整成funtion
    """
    原本在event.py頂端就有 with open，但這裡沒有，所以搬過來看看是否正常
    此功能主要 隨機選擇 json檔案裡 指定key裡隨機value
    """
    with open('mumi_setting.json','r',encoding='utf8') as jfile:
        jdata = json.load(jfile)
    
    #if random.randint(1,100) > random.randint(40,50):
    react_rand = random.choice(jdata[json_document])
    return msg.channel.send(react_rand, reference = msg , mention_author = False)



def upload_photo(image_url,what_album):
    """
    避免fb scraper抓到的圖檔死去，先上傳至imgur 再由mumibot傳送該imgur網址

    """
    client_id = ''
    client_secret = ''
    access_token = ''
    refresh_token = ''
    client = ImgurClient(client_id, client_secret, access_token, refresh_token)
    album = what_album # You can also enter an album ID here
    config = {
  'album': album,
 }

    print("Uploading image... ")
    image = client.upload_from_url(image_url, config=config, anon=False)
    print("Done")    
    return image['link']


def get_server(req_address,req_id,server_info,server_value): #server_value 這邊抓channel_id  #抓server避免重複頻道ID一直上傳
    """
    獲取指定server的所有資訊 (根據帶入的資料)，我這邊用意是抓取特定伺服器 所有channel id
    """
    response = requests.get(req_address,{"id":req_id})
    data = response.json()
    server_id = []
    for server in range(0,len(data[0][server_info])):
        server_id.append(data[0][server_info][server][server_value])
    return server_id


def discord_append(address,ad_id,num,n_key,**kwargs):#channel_info追加用
    """
    增加使用權限的 channel 或是 user
    """
    response = requests.get(address,{"id":ad_id}) 

    data = response.json()
    #回傳給json如個是字串 要用f"{}"包起來
    
    try_get_channel = kwargs.get('channel_guild',[])
    try_get_user = kwargs.get('bot_user_id',[])
    try_get_url = kwargs.get('url',[])
    try_get_n_url = kwargs.get('n_url',[])
    # 改天來測試一下這裡變數在幹嘛
    if type(try_get_channel) != list:
        content = {"channel_guild":kwargs.get('channel_guild',[]),
        "channel_name":kwargs.get('channel_name',[]),
        "channel_id":kwargs.get('channel_id',[])}

    elif type(try_get_user) != list:
        content = {"bot_user_name":kwargs.get('bot_user_name',[]),
        "bot_user_id":kwargs.get('bot_user_id',[])}
    
    elif type(try_get_url) != list: 
        content = {"url":kwargs.get('url',[]),
        "datetime":kwargs.get('datetime',[]),
        "unicode":kwargs.get('unicode',[]),
        "type":kwargs.get('type',[])} # 追加
    
    elif type(try_get_n_url) != list: 
        content = {"n_url":kwargs.get('n_url',[]),
        "n_datetime":kwargs.get('n_datetime',[]),
        "n_unicode":kwargs.get('n_unicode',[]),
        "n_type":kwargs.get('n_type',[])} 
        
    else:
        pass
    
    data[num][n_key].append(content)

    return data

def discord_pop(address,ad_id,num,n_key,*arg):#channel_info追加用
    """
    去除使用權限的 channel 或是 user
    """
    response = requests.get(address,{"id":ad_id}) 
    data = response.json()
    dict_len =   len(data[num][n_key])
    for key in arg:
        if key == 'channel_id':
            for number in range(0,dict_len):
                if data[num][n_key][number]['channel_id'] == arg[1] :
                    data[num][n_key].pop(number)
                    break
        elif key =='bot_user_id':
            for number in range(0,dict_len):
                if data[num][n_key][number]['bot_user_id'] == arg[1] :
                    data[num][n_key].pop(number)
                    break
    return data      

    #                           ID 可能為 使用者 或 頻道
    #arg目前暫定順序 (新增/刪除 , ID ,  哪個key )

def discord_upd(address,ad_id,num,n_key,*arg,**kwargs):    #上傳至雲端json #channel_info上傳用
    """
    將資料上傳至 雲端json
    """
    if arg[0] == 0 : # 0 增加資料  #arg[0] 用來觀看是要增加還是刪除 
        update = requests.put(address,  #arg[1] 放 ID
        params =   {"id":ad_id},
        json = discord_append(address,ad_id,num,n_key,**kwargs)
        )
    elif arg[0] == 1 : # 1 刪除資料
        update = requests.put(address,
        params =   {"id":ad_id},
        json = discord_pop(address,ad_id,num,n_key,*arg)
        )


def res_append(scrap_id,scrap_datetime,address,ad_id,scrap_fb):
    '''
    上傳到雲端json，根據傳來的參數(azure、honkai、wflipper、maple)，來帶入各個排版，最後回傳整理好的資料(data)
    '''
    response = requests.get(address,{"id":ad_id}) #新增value(疊加

    data = response.json()
    if scrap_fb == "azure":
        content = {"azure_id":scrap_id,"azure_datetime":scrap_datetime}
    elif scrap_fb == "honkai":
        content = {"honkai_id":scrap_id,"honkai_datetime":scrap_datetime}
    elif scrap_fb == "wflipper":
        content = {"wflipper_id":scrap_id,"wflipper_datetime":scrap_datetime}
    elif scrap_fb == "maple":
        content = {"maple_id":scrap_id,"maple_datetime":scrap_datetime}
    else:
        pass
    data.append(content)
    return data


def some_list(what_key,req_address,req_id,*arg): #將json裡的某個值放進list
    '''
    取得該json每一個指定value(這邊抓時間的value)，將每一個key值得value抓出來放到一個list，最後回傳該list
    arg[0] 使用的json有 : honkai_json、楓之谷_json、Azure_json
    arg[1] 使用的json有 : mix_json、img_download
    '''
    response = requests.get(req_address,{"id":req_id})
    data = response.json()
    someList=[]
    if arg[0] == 0 :
        for i in range(0,len(data)):
            someList.append(data[i][what_key])
    elif arg[0] == 1 : 
        data = data[0][arg[1]]  # data賦予新值，避免下面又要下太長
        for i in range(0,len(data)): # 抓取data指定資料的range 總共要讓for迴圈跑幾次
            someList.append(data[i][what_key]) # 最後將抓到的資料全部放到LIst裡
    else:
        print("值帶錯了吧，87")
        pass
    return someList     # 回傳值

def upd(up_id,up_datetime,address,ad_id,scrap_fb):    #上傳至雲端json
    '''
    將資料上傳(更新)至指定的json資料庫
    '''
    update = requests.put(address,
    params =   {"id":ad_id},
    json = res_append(up_id,up_datetime,address,ad_id,scrap_fb)
    )


def printError(e,taskString): 
    '''
    能夠抓到報錯的資料
    取得該發生錯誤的行數和什麼error
    '''
    error_class = e.__class__.__name__ #取得錯誤類型
    detail = e.args[0] #取得詳細內容
    cl, exc, tb = sys.exc_info() #取得Call Stack
    lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
    fileName = lastCallStack[0] #取得發生的檔案名稱
    lineNum = lastCallStack[1] #取得發生的行號
    funcName = lastCallStack[2] #取得發生的函數名稱
    #  print("_______________________This is Error____________________")
    errMsg = "________File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
    print(taskString,errMsg)

def BannedError(count,BannedWarning):  
    '''
     如果 被FB Ban，每發生一次 temporarily banned ，就睡10分鐘 第二次就 20分鐘，直到解除被ban
    '''
    count +=1
    sleep_secs = 600 * count
    print(f"{BannedWarning} {sleep_secs / 60} m ({sleep_secs} secs)")
    return  sleep_secs
#print(f"Temporarily banned, sleeping for {sleep_secs / 60} m ({sleep_secs} secs)")



def random_sleep(first,second):
    '''
    隨機冷卻時間應用
    '''
    result = random.randint(first,second)
    return result


def set_timeznoe(timezone):
    '''
    抓時間
    '''
    utc_time = dt.utcnow()
    local_time = utc_time + timedelta(hours=timezone)
    return local_time
