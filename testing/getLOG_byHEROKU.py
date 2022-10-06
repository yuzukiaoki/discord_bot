import os,time
from datetime import datetime

#nowTime = datetime.now().strftime("%Y-%m-%d_%H：%M")
while True:
    nowTime = datetime.now().strftime("%H：%M")
    WholenowTime = datetime.now().strftime("%Y-%m-%d_%H：%M")
    
    if nowTime == "08：30": #每天早上8.30 輸出log
        os.system(f"heroku logs -n 1500 --app mumibot > C:\\Users\\Administrator\\Documents\\GitHub\\mumi_bot\\logs\\{WholenowTime}_mumibotLOG.txt")
        print(WholenowTime)        # 換heroku時 記得換 APP 名稱
        print("Ready to sleep :>")        
        time.sleep(84600) #睡23小時又30分
    print(f"{WholenowTime} still looping 0.0")
    time.sleep(30)
# print("wonderful")
# #print(nowTime)

# thetime = datetime.now().strftime("%H：%M")
# print(thetime)
# #os.system("heroku logs -n 1500 --app mumibot >> C:\\Users\\Administrator\\Documents\\GitHub\\mumi_bot\\logs\\mumibotLOG.txt")
# a=0
# b=10
# while True:
#     print('loop')
#     a +=1
#     if a == b:
#         print('great')
#         break
