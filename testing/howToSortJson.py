import json
'''
如何將 JSON檔案 只有一排的狀況 變成縮排的樣子
https://ithelp.ithome.com.tw/articles/10216970
https://officeguide.cc/python-read-write-json-encode-decode-tutorial-examples/

'''

with open('response.json', newline='') as jsonfile: #讀取要排版的json
    data = json.load(jsonfile)   #把該json 賦予變數


with open("response.json", "w") as f: #改寫該json  
    json.dump( data,f, indent = 4)   #寫入他

