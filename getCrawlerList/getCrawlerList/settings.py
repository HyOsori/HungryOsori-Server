# Scrapy settings for getCrawlerList project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

import sys
import os

import django
from django.conf import settings
DJANGO_PROJECT_PATH = '/home/ubuntu/django/crawlerAPI'
DJANGO_SETTINGS_MODULE = 'crawlerAPI.settings'
if DJANGO_PROJECT_PATH not in sys.path:
    sys.path.append(DJANGO_PROJECT_PATH)
#os.environ['DJANGO_SETTINGS_MODULE'] = DJANGO_SETTINGS_MODULE

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crawlerAPI.settings')
django.setup()


ITEM_PIPELINES = {
    'getCrawlerList.pipelines.GetcrawlerlistPipeline' : 1000,
}

SPIDER_MODULES = ['getCrawlerList.spiders',]
NEWSPIDER_MODULE = 'getCrawlerList.spiders'

