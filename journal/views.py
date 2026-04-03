from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.contrib import messages
from django.urls import reverse

from actionhealth.permissions import can_modify_owned_content

from .forms import AddJournalForm
from .models import Journal

def all_journals(request):
    journals = Journal.objects.filter(is_published=True)
    return render(request, 'journal/all_journals.html', {'journals': journals})  

@login_required
def add_journal(request):
    form = AddJournalForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            journal = form.save(commit=False)

            journal.user = request.user
            journal.is_published = True
            journal.save()

            messages.success(request, 'journal addded Sucessfully')
            return redirect(reverse('journal:journal_detail', kwargs={'slug':journal.slug}))
    context = {'form': form}
    return render(request, 'journal/add_journal.html', context)

def journal_detail(request, slug):
    journal = get_object_or_404(Journal, slug=slug)
    if not journal.is_published:
        user = request.user
        if not user.is_authenticated or not can_modify_owned_content(user, journal.user_id):
            raise Http404()

    author = journal.user
    author_journals = Journal.objects.filter(user=author, is_published=True)[:4]
    related_journals = Journal.objects.filter(user=author, is_published=True)[:0]
    context = {
        'journal': journal,
        'author_journals': author_journals,
        'related_journals': related_journals,
    }
    return render(request, 'journal/journal_detail.html', context)

@login_required
def edit_journal(request, slug):
    journal = get_object_or_404(Journal, slug=slug)
    if not can_modify_owned_content(request.user, journal.user_id):
        raise PermissionDenied
    form = AddJournalForm(request.POST or None, instance=journal)
    if request.method == 'POST':
        if form.is_valid():
            journal = form.save(commit=False)
            journal.save()

            messages.success(request, 'journal edited sucessfully')
            return redirect(reverse('journal:journal_detail', kwargs={'slug':journal.slug}))
    context = {'form': form}
    return render(request, 'journal/edit_journal.html', context)