from django.shortcuts import render

from journal.models import Journal
from article.models import Article
from event.models import Event

# Create your views here.

def index(request):
    journals = Journal.objects.filter(is_published=True)[:4]
    events = Event.objects.filter(is_published=True)[:4]
    context = {
        'journals':journals,
        'events': events,
    }
    return render(request, 'base/index.html', context)

def journals(request):
    return render(request, 'base/journals.html', {})

def articles(request):
    articles = Article.objects.filter(is_published=True)
    return render(request, 'base/articles.html', {'articles': articles})

def honorees(request):
    return render(request, 'base/honorees.html', {})

def trainings(request):
    return render(request, 'base/trainings.html', {})

def events(request):
    return render(request, 'base/events.html', {})

def memberships_info(request):
    return render(request, 'base/memberships_info.html', {})
