import time
import arrow

def time_now():
    return arrow.now().format('YYYY-MM-DD HH:mm:ss')


def sleep_min(min):
    time.sleep( min * 60 )
