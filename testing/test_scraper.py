from facebook_scraper import get_posts
#from imgur_test import *
#from testing.imgur_test.imgur_upload_test import upload_imgur
import time
"""
嘗試 facebookscarper能不能用
"""

# for post in get_posts('bh3TW', pages=2):

#     print(post['text'][:50])
#     for i in post['images']:
#         print(i)
#         print(type(i))
#     print(post['post_id'])
post_list = get_posts("bh3TW", pages=2)

if post_list is not None:
    for post in post_list:
        #print(type(post['images']))
        #print(post['images'])
        print(post['images'])
        #print()
        # if post['images'] is not None:
        #     #print(post['images'])
        #     for image in post['images']:
        #         # upload_imgur(image)
        #         # time.sleep(2)
        #         print(image)
        #         #print(type(image))