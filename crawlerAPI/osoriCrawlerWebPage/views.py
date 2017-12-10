from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from django.views.generic import TemplateView, ListView
from osoriCrawlerAPI.models import Crawler, Subscription


class LoginView(TemplateView):
    template_name = "osoriCrawlerAPI/main.html"


class UserCrawlerView(ListView):
    permission_classes = (IsAuthenticated,)
    model = Crawler
    template_name = "osoriCrawlerAPI/user_crawler.html"
