import requests


response = requests.get('https://jsonstorage.net/api/items/7c3e00f2-bc8c-4df3-b30f-6a6f7ea59659',{
    "id":"7c3e00f2-bc8c-4df3-b30f-6a6f7ea59659"
})

data = response.json()
tet = {"id":123456789,"datetime":"2020-02-03"}
data.append(tet)

update = requests.put('https://jsonstorage.net/api/items/7c3e00f2-bc8c-4df3-b30f-6a6f7ea59659',
params =   {"id":"7c3e00f2-bc8c-4df3-b30f-6a6f7ea59659"},
json = data
) 

print(update)
