from django.urls import path
from .views import add_article, all_articles, article_detail

app_name = 'article'

urlpatterns = [
    path('', all_articles, name='all_articles'),
    path('all/', all_articles, name='all_articles'),
    path('all_articles/', all_articles, name='all_articles'),
    path('add/', add_article, name='add_article'),
    path('<slug:slug>/', article_detail, name='article_detail'),
]
