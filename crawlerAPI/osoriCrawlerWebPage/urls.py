from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

''' There are many things to fix url to right rules and proper type! '''

urlpatterns = [
    url(r'^$', LoginView.as_view(), name='main'),
    url(r'^user_crawler/$', UserCrawlerView.as_view(), name='user_crawler'),
]

urlpatterns = format_suffix_patterns(urlpatterns)