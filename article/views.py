from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

from .forms import AddArticleForm
from .models import Article

def all_articles(request):
    articles = Article.objects.filter(is_published=True)
    return render(request, 'article/all_articles.html', {'articles': articles})    

@login_required
def add_article(request):
    form = AddArticleForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            article = form.save(commit=False)

            article.user = request.user
            article.is_published = True
            article.save()

            messages.success(request, 'Article addded Sucessfully')
            return redirect(reverse('article:article_detail', kwargs={'slug':article.slug}))
    context = {'form': form}
    return render(request, 'article/add_article.html', context)

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    
    author = article.user
    author_articles = Article.objects.filter(user=author, is_published=True)[:4]
    related_articles = Article.objects.filter(user=author, is_published=True)[:0]
    context = {
        'article': article,
        'author_articles': author_articles,
        'related_articles': related_articles,
    }
    return render(request, 'article/article_detail.html', context)
