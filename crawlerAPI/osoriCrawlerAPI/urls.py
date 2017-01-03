from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from osoriCrawlerAPI import views

''' There are many things to fix url to right rules and proper type! '''

urlpatterns = [
    url(r'^users/$', views.UserList.as_view()),
    url(r'^user/$', views.UserDetail.as_view()),
    url(r'^crawlers/$', views.CrawlerList.as_view()),
    url(r'^crawler/$', views.CrawlerDetail.as_view()),
    url(r'^subscriptions/$', views.SubscriptionList.as_view()),
    url(r'^subscription/$', views.SubscriptionDetail.as_view()),
    url(r'^pushtokens/$', views.PushTokenList.as_view()),
    url(r'^pushtoken/$', views.PushTokenDetail.as_view()),
    url(r'^email_auth/(?P<auth>.+)/$', views.Auth.email_auth),
    url(r'^password/$', views.Password.as_view()),
    url(r'^subscribers_pushtoken/$', views.SubscriberPushToken.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)