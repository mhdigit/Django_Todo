
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import time


class WeatherDetail(APIView):

    @method_decorator(cache_page(60*20))
    def get(self, request, loc, format=None):
        res = requests.get(f'https://wttr.in/{loc}?format=j1').json()
        text = requests.get(f'https://wttr.in/{loc}?format=4')
        res['simple'] = text
        time.sleep(5)

        return Response(res)


class WeatherDetailView(TemplateView):

    template_name = "weather/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["loc"] = kwargs['loc']
        return context
