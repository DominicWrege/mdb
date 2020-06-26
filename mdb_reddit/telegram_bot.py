
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep
from dotenv import load_dotenv
import os
from mdb_reddit.util import get_reddit_db, get_kafka_consumer

from telegram.ext import Updater, CommandHandler

def main():
    load_dotenv()
    token = os.getenv("TELEGRAM_TOKEN")
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()

def start(update, context):
    update.message.reply_text('Hi! Use /set <seconds> to set a timer')


if __name__ == '__main__':
    main()