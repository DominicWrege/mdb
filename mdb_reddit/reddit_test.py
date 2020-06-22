#
# Just for playing with reddit api 
#

import praw
import json 
import math
import arrow


def runner():
    print("runn")

def runn(runner):
    runner()


def main():

    print(arrow.now().format('YYYY-MM-DD HH:mm:ss'))
    runn(runner)
    reddit = praw.Reddit(client_id="ZuAQ4z82JQDngA",
                        client_secret="yzTKHSRGbl0O8ROCq2oi1gnX8vA",
                        user_agent="my user agent")
    #reddit.front.top(time_filter="day", limit=10):
    #reddit.front.hot(limit=10):
    #reddit.front.controversial(time_filter="day", limit=10):
    #reddit.front.rising(limit=10)
    for submission in reddit.front.rising(limit=10):
        #print("title:", submission.title, "  url:", submission.url)
        post_j = json.dumps({"title": submission.title, "url": submission.url})
        print(post_j)

if __name__ == "__main__":
    main()

    