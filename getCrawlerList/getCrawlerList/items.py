# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field
from scrapy_djangoitem import DjangoItem

from osoriCrawlerAPI.models import Crawler


class CrawlerItem(DjangoItem):
    # define the fields for your item here like:
    # name = Field()
    django_model = Crawler
