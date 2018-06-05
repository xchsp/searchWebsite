from scrapy.cmdline import execute
from redis import Redis

import os
import sys
import threading
import time


sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def push_start():
    while True:
        print("pusher running now")
        time.sleep(2000)
        redis.lpush('freebuf_slave:start_url', "http://www.freebuf.com")

def run():
    execute(['scrapy', 'crawl', 'freebuf_slave_spider'])


if __name__ == '__main__':
    redis = Redis(host="10.10.10.1")

    t1 = threading.Thread(target=push_start)
    t1.start()
    run()
    
# execute(['scrapy', 'crawl', 'freebuf_slave_spider'])
