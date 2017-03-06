from scrapy.spiders import Spider
import scrapy
from getCrawlerList.items import crawlerItem
import json

class CrawlerSpider(scrapy.Spider):
    name = "CrawlerSpider"
    allowed_domains = ["github.com"]
    start_ulrs = ['http://raw.githubusercontent.com/HyOsori/Osori-WebCrawler/master/settings.json']
    def start_requests(self):
        urls = [
            'http://raw.githubusercontent.com/HyOsori/Osori-WebCrawler/master/settings.json'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        content = response.url.split("/")[-2]       
        filename = 'crawlers.json'
        with open(filename, 'wb') as f:
            f.write(response.body)
        with open('crawlers.json') as crawler_file:
            data = json.load(crawler_file)
        crawlers=data.values()
        for crawler in crawlers:
            yield crawlerItem(crawler_id=crawler['crawl_id'], thumbnail_url=crawler['thumbnail'], link_url=crawler['link_url'], title=crawler['title'], description=crawler['desc'])
