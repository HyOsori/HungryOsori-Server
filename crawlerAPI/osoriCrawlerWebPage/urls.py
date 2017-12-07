from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from osoriCrawlerWebPage import views

''' There are many things to fix url to right rules and proper type! '''

urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^user_crawler$', name='user_crawler'),
]

urlpatterns = format_suffix_patterns(urlpatterns)