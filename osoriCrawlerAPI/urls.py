from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from osoriCrawlerAPI import views

urlpatterns = [
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/find/$', views.UserDetail.as_view()),
    url(r'^crawlers/$', views.CrawlerList.as_view()),
    url(r'^crawlers/(?P<name>)/$', views.CrawlerDetail.as_view()),
    url(r'^subscriptions/$', views.SubscriptionList.as_view()),
    url(r'^subscriptions/item/$', views.SubscriptionDetail.as_view()),
    url(r'^tokens/$', views.PushTokenList.as_view()),
    url(r'^tokens/(?P<id>[a-z0-9]+)/$', views.PushTokenDetail.as_view()),
    url(r'^login/$', views.Login.as_view()),
    url(r'^logout/$', views.Login.as_view()),
    url(r'^email_auth/(?P<auth>.+)/$', views.Auth.email_auth),
]

urlpatterns = format_suffix_patterns(urlpatterns)