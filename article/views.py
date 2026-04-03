from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.contrib import messages
from django.urls import reverse

from actionhealth.permissions import can_modify_owned_content

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
    if not article.is_published:
        user = request.user
        if not user.is_authenticated or not can_modify_owned_content(user, article.user_id):
            raise Http404()

    author = article.user
    author_articles = Article.objects.filter(user=author, is_published=True)[:4]
    related_articles = Article.objects.filter(user=author, is_published=True)[:0]
    context = {
        'article': article,
        'author_articles': author_articles,
        'related_articles': related_articles,
    }
    return render(request, 'article/article_detail.html', context)

@login_required
def edit_article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if not can_modify_owned_content(request.user, article.user_id):
        raise PermissionDenied
    form = AddArticleForm(
        request.POST or None, request.FILES or None, instance=article
    )
    if request.method == 'POST':
        if form.is_valid():
            article = form.save(commit=False)
            article.save()

            messages.success(request, 'article edited sucessfully')
            return redirect(reverse('article:article_detail', kwargs={'slug':article.slug}))
    context = {'form': form}
    return render(request, 'article/edit_article.html', context)