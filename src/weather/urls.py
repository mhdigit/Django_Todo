# from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from django.urls import path, include
from django.views.generic.base import RedirectView

from . import views

app_name = "weather"


urlpatterns = [
    path('api',  RedirectView.as_view(
        url='/weather/api/tehran')),
    path('api/',  RedirectView.as_view(
        url='/weather/api/tehran')),


    path('',  RedirectView.as_view(
        url='/weather/tehran')),

    path('<str:loc>', views.WeatherDetailView.as_view()),


    path('api/<str:loc>', views.WeatherDetail.as_view(), name='weather_detail'),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
