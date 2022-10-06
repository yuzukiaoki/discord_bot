# from data_file.get_something import get_server
# def get_server(req_address,req_id,server_info,server_value): #server_value 這邊抓channel_id
#     response = requests.get(req_address,{"id":req_id})
#     data = response.json()
#     server_id = []
#     for server in range(0,len(data[0][server_info])):
#         server_id.append(data[0][server_info][server][server_value])
#     return server_id
# aser = get_server(
#     "https://jsonstorage.net/api/items/0bb0a3f0-2274-4699-9834-4d9a9a027d19"
#     ,"0bb0a3f0-2274-4699-9834-4d9a9a027d19","bot_user","bot_user_id")
# print('--'*20)

# print(aser)

#[0]["channel_info"][1]["channel_id"]
import requests

response = requests.get('https://api.jsonstorage.net/v1/json/cc3a38bc-d03a-43bd-b2dc-0d4127034cf1/a1100173-e266-4101-b509-e828607176b2?apiKey=79d12025-f3e5-4ce8-bb29-6dbd4d956d4d',{
    "id":"a1100173-e266-4101-b509-e828607176b2?apiKey=79d12025-f3e5-4ce8-bb29-6dbd4d956d4d"
})
print(response.json())

"""
測試 request posman怎麼用
"""