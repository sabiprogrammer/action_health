from django.urls import path
from .views import add_journal, all_journals, journal_detail

app_name = 'journal'

urlpatterns = [
    path('', all_journals, name='all_journals'),
    path('all_journals/', all_journals, name='all_journals'),
    path('add/', add_journal, name='add_journal'),
    path('<slug:slug>/', journal_detail, name='journal_detail'),
]
