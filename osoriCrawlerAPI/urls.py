from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from osoriCrawlerAPI import views

urlpatterns = [
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<id>[a-z0-9]+)/$', views.UserDetail.as_view()),
    url(r'^crawlers/$', views.CrawlerList.as_view()),
    url(r'^crawlers/(?P<name>[a-z0-9]+)/$', views.CrawlerDetail.as_view()),
    url(r'^subscriptions/$', views.SubscriptionList.as_view()),
    url(r'^subscriptions/find/$', views.SubscriptionDetail.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)