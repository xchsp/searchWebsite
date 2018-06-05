from redis import Redis
from scrapy.http import Request
from urllib import parse
from scrapy_redis.spiders import RedisSpider
from ..items import FreebufItem, ArticleItemLoader


class FreebufMasterSpider(RedisSpider):
    name = 'freebuf_master_spider'
    # read urls from redis
    redis_key = 'freebuf:start_url'

    def parse(self, response):
        redis = Redis()
        redis.lpush('freebuf_slave:start_url', response.url)
        next_url = response.css("#pagination a::attr(href)").extract_first()
        if next_url and "page" in next_url:
            yield Request(url=parse.urljoin(response.url, next_url),
                          callback=self.parse,
                          method="POST")


class FreebufSlaveSpider(RedisSpider):
    name = 'freebuf_slave_spider'
    allowed_domains = ['www.freebuf.com']
    # read urls from redis
    redis_key = 'freebuf_slave:start_url'

    def parse(self, response):
        urls = response.css("div.news-img a[target=_blank]::attr(href)").extract()

        for url in urls:
            # yield self.make_requests_from_url(url)
            yield Request(url=parse.urljoin(response.url, url),
                          callback=self.parse_article)

    def parse_article(self, response):
        item_loader = ArticleItemLoader(item=FreebufItem(), response=response)
        item_loader.add_value("url", response.url)
        item_loader.add_css("title", "title::text")
        item_loader.add_css("author", ".author-name::text")
        item_loader.add_css("create_time", ".property .time::text")
        # item_loader.add_css("tags", ".tags a::text")
        item_loader.add_css("html_content", "#contenttxt")

        freebuf_article_item = item_loader.load_item()

        yield freebuf_article_item