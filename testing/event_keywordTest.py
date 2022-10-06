
ctx_message = "hello peko sao"

check_map = { # 把關鍵字整理成一個map
    "caution_floor":{ # 為這組關鍵字取個一名字，類似取function名，隨便都行
        "trigger":["peko","hololive"], # 要觸發的關鍵字 list
        "action":lambda: print("好油喔") # 觸發時要做的行動，別管lambda是啥，反正丟在lambda後面就對了，可以丟define
    },
    "shi":{ #另一組
        "trigger":["sao","starburst"],
        "action":lambda: print("噓")
    }
}

trigger_count = 0 # 記錄觸發次數，避免一句話如果 sao 跟 peko 同時存在，會回復兩次訊息
for key in check_map:
    if trigger_count > 0: # 有記錄代表有觸發過，就別執行了
        break
    key_words = check_map[key].get("trigger",[])
    for word in key_words:

        if word in ctx_message:
            print(key_words)
            print(type(key_words))
            print(word)
            print(type(word))
            check_map[key]["action"]()
            trigger_count += 1 # 有觸發就加1
            break # 如果已經找到同組的關鍵字，就不用再找了