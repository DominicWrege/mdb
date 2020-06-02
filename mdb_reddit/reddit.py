#
# Just for playing with reddit api 
#

import praw
import json 
import math


reddit = praw.Reddit(client_id="ZuAQ4z82JQDngA",
                     client_secret="yzTKHSRGbl0O8ROCq2oi1gnX8vA",
                     user_agent="my user agent")


for submission in reddit.front.top(time_filter="day", limit=10):
    #print("title:", submission.title, "  url:", submission.url)
    post_j = json.dumps({"title": submission.title, "url": submission.url})
    print(post_j)



    