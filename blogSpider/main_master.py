from scrapy.cmdline import execute
from redis import Redis

import os
import sys


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
redis = Redis(host="10.10.10.1")
redis.lpush('freebuf:start_url', 'http://www.freebuf.com')
execute(['scrapy', 'crawl', 'freebuf_master_spider'])
