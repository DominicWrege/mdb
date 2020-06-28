
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep
from dotenv import load_dotenv
import os
from mdb_reddit.util import get_kafka_consumer, time_now
import json
from telegram.ext import Updater, CommandHandler 
from uuid import uuid4
import logging
import threading
import pdb
from queue import Queue, Empty
import redis
from redis.client import Redis

send_queue = Queue()
db_password = ""
connection_pool = None


def main():
    global connection_pool
    global db_password
    load_dotenv()
    token = os.getenv("TELEGRAM_TOKEN")
    db_password = os.getenv("REDIS_PWD")
    print("Starting Telegram Bot")
    updater = Updater(token, use_context=True)
    connection_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0, password=db_password, max_connections=16)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("sub", subscribe, pass_args=True))
    dp.add_handler(CommandHandler("unsub", unsubscribe, pass_args=True))
    dp.add_handler(CommandHandler("hello", greeting))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("list", list_subs))
    threading.Thread(target=kafka, args=([])).start()
    updater.job_queue.run_repeating(poll, 6)
    updater.start_polling()
    updater.idle()


def con_redis():
    global connection_pool
    return Redis(connection_pool=connection_pool)

def poll(context):
    global send_queue
    while True:
        try:
            item = send_queue.get_nowait()
            context.bot.send_message(item[0], text=item[1])
            sleep(0.5)
        except Empty:
            break

def greeting(update, context):
    username = update.message.chat.username
    update.message.reply_text(
        f"Hey {username} 👋 my name is Guido 🦔 and I am your reddit bot.\nYou can use /help for more information."
        )
def help(update, context):
    msg = """Commands:
/sub <subreddit_name> \t to subscribe
/unsub <subreddit_name>...\t to unsubscribe
/list \t show your subscriptions
/hello greetings to you =)
            """
    update.message.reply_text(msg)

def list_subs(update, context):
    db = con_redis()
    user_id = update.message.chat.id
    subscriptions = db.smembers(user_id)
    if len(subscriptions) == 0:
        update.message.reply_text("You have no subscriptions")
    else:
        msg = list()
        for item in subscriptions:
            msg.append(item.decode("UTF-8"))
        update.message.reply_text(f"Your subscriptions: {', '.join(msg)}")

def need_more_arguments(update):
    if hasattr(update.message, 'reply_text'):
            update.message.reply_text("Need 1 argument <subredditname>")

def subscribe(update, context):
    # update.message.reply_text('Hi! Use /set <dsa to set a timer')
    if len(context.args) < 1:
        update.message.reply_text("Need 1 argument <subredditname>")
        return
    b_subreddit_name = context.args[0].encode("UTF-8")
    subreddit_name = context.args[0]
    user_id = update.message.chat.id
    redis = con_redis()
    subscriptions = redis.smembers(user_id)
    print(subscriptions)
    if b_subreddit_name in subscriptions:
        update.message.reply_text(f"You are already subscribed to {subreddit_name}")
    else:
        redis.sadd(user_id, b_subreddit_name)
        update.message.reply_text(f"Successfully subscribed to '{subreddit_name}'  🦊")

def unsubscribe(update, context):
    if len(context.args) < 1:
        need_more_arguments(update)
        return
    db = con_redis()
    user_id = update.message.chat.id
    subs = db.smembers(user_id)
    if len(subs) == 0:
        update.message.reply_text(f"You have 0 subscriptions.")
        return
    removed = []
    for arg in context.args:
        b_arg = arg.encode("UTF-8")
        if b_arg in subs:
            db.srem(user_id, b_arg)
            removed.append(arg)
    if len(removed) == 0:
        update.message.reply_text("Nothing Removed.")
    else:
        update.message.reply_text(f"Removed: {', '.join(removed)}")
    update.message.reply_text("Done 🐊")


def kafka():
    db = con_redis()
    for msg in get_kafka_consumer("telegram"):
        print(f"{time_now()} - Getting messages from Kafka")
        post = json.loads(msg.value.decode("UTF-8"))
        for user_id in db.scan_iter("*"):
            user_subs = db.smembers(user_id)
            if post["subbredit"].encode("UTF-8") in user_subs:
                str_msg = f"{post['title']} ({post['subbredit']})\nurl: {post['url']}\nscore: {post['score']}"
                send_message(user_id.decode('utf8'), str_msg)


def send_message(user_id, data):
    send_queue.put((user_id, data))


if __name__ == '__main__':
    main()


