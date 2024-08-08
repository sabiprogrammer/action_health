from django.urls import path
from .views import (
    index, journals, articles, honorees,
    trainings, events, memberships_info
    )

app_name = 'base'

urlpatterns = [
    path('', index, name='index'),
    path('journals/', journals, name='journals'),
    path('articles/', articles, name='articles'),
    path('honorees/', honorees, name='honorees'),
    path('trainings/', trainings, name='trainings'),
    path('events/', events, name='events'),
    path('memberships/', memberships_info, name='memberships_info'),
]
