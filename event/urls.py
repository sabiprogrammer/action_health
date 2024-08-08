from django.urls import path
from .views import add_event, all_events, event_detail

app_name = 'event'

urlpatterns = [
    path('', all_events, name='all_events'),
    path('all/', all_events, name='all_events'),
    path('all_events/', all_events, name='all_events'),
    path('add/', add_event, name='add_event'),
    path('<slug:slug>/', event_detail, name='event_detail'),
]
