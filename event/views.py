from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.contrib import messages
from django.urls import reverse

from actionhealth.permissions import can_modify_owned_content

from .forms import AddEventForm
from .models import Event

def all_events(request):
    events = Event.objects.filter(is_published=True)
    return render(request, 'event/all_events.html', {'events': events})    

@login_required
def add_event(request):
    form = AddEventForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            event = form.save(commit=False)

            event.user = request.user
            event.is_published = True
            event.save()

            messages.success(request, 'Event addded Sucessfully')
            return redirect(reverse('event:event_detail', kwargs={'slug':event.slug}))
    context = {'form': form}
    return render(request, 'event/add_event.html', context)

def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug)
    if not event.is_published:
        user = request.user
        if not user.is_authenticated or not can_modify_owned_content(user, event.user_id):
            raise Http404()

    author = event.user
    # author_events = Event.objects.filter(user=author, is_published=True)[:4]
    related_events = Event.objects.filter(is_published=True)[:4]
    context = {
        'event': event,
        'related_events': related_events,
    }
    return render(request, 'event/event_detail.html', context)


@login_required
def edit_event(request, slug):
    event = get_object_or_404(Event, slug=slug)
    if not can_modify_owned_content(request.user, event.user_id):
        raise PermissionDenied
    form = AddEventForm(request.POST or None, request.FILES or None, instance=event)
    if request.method == 'POST':
        if form.is_valid():
            event = form.save(commit=False)
            event.save()

            messages.success(request, 'event edited sucessfully')
            return redirect(reverse('event:event_detail', kwargs={'slug':event.slug}))
    context = {'form': form}
    return render(request, 'event/edit_event.html', context)