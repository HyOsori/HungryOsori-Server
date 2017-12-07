from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from osoriCrawlerAPI import views
from django.contrib import admin
from rest_framework.authtoken import views as auth_token_views

''' There are many things to fix url to right rules and proper type! '''

urlpatterns = [
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^signup/$', views.SignUp.as_view(), name='signup'),
    url(r'^social_sign/$', views.SocialSign.as_view(), name='social_sign'),
    url(r'^signin/$', views.SignIn.as_view(), name='signin'),
    url(r'^logout/$', views.Logout.as_view(), name='logout'),
    url(r'^user/$', views.UserDetail.as_view(), name='user'),
    url(r'^crawlers/$', views.CrawlerList.as_view()),
    url(r'^crawler/$', views.CrawlerDetail.as_view()),
    url(r'^subscriptions/$', views.SubscriptionList.as_view()),
    url(r'^subscription/$', views.SubscriptionDetail.as_view()),
    url(r'^pushtokens/$', views.PushTokenList.as_view()),
    url(r'^pushtoken/$', views.PushTokenDetail.as_view()),
    url(r'^email_auth/(?P<auth>.+)/$', views.Auth.email_auth),
    url(r'^password/$', views.Password.as_view()),
    url(r'^subscribers_pushtoken/$', views.SubscriberPushToken.as_view()),


]

urlpatterns = format_suffix_patterns(urlpatterns)