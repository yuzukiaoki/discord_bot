import requests

def res_append(key1,value1):
    response = requests.get('https://jsonstorage.net/api/items/f433848e-27e5-4765-882f-d0a967a06c9e',{
        "id":"f433848e-27e5-4765-882f-d0a967a06c9e"
    })

    data = response.json()
    data[key1].append(value1)
    return data

def res(key2,value2):
    response = requests.get('https://jsonstorage.net/api/items/f433848e-27e5-4765-882f-d0a967a06c9e',{
        "id":"f433848e-27e5-4765-882f-d0a967a06c9e"
    })

    data = response.json()
    data[key2] = value2
    return data




def upd():
    update = requests.put('https://jsonstorage.net/api/items/f433848e-27e5-4765-882f-d0a967a06c9e',
    params =   {"id":"f433848e-27e5-4765-882f-d0a967a06c9e"},
    json = res("ina",["cute","bang"])
    ) 

    print(update)

upd()
