from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from sgce.core.forms import EventForm
from sgce.core.mixins import EventCreatedByPermission
from sgce.core.models import Event
from sgce.core.utils.get_deleted_objects import get_deleted_objects


@login_required
def index(request):
    return render(request, 'core/index.html')


class EventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'core/event/list.html'
    context_object_name = 'events'

    def get_queryset(self):
        queryset = super(EventListView, self).get_queryset()
        user = self.request.user
        return queryset if user.is_superuser else queryset.filter(created_by = self.request.user)


class EventCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Event
    form_class = EventForm
    permission_required = 'core.add_event'
    raise_exception = True
    template_name = 'core/event/form.html'
    success_url = reverse_lazy('core:event-list')
    success_message = "O evento %(name)s foi criado com sucesso."

    def form_valid(self, form):
        obj = form.save(commit = False)
        obj.created_by = self.request.user
        return super(EventCreateView, self).form_valid(form)


class EventUpdateView(LoginRequiredMixin, EventCreatedByPermission, SuccessMessageMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'core/event/form.html'
    success_url = reverse_lazy('core:event-list')
    success_message = "O evento %(name)s foi atualizado com sucesso."


class EventDeleteView(LoginRequiredMixin, EventCreatedByPermission, DeleteView):
    model = Event
    form_class = EventForm
    template_name = 'core/event/delete.html'
    success_url = reverse_lazy('core:event-list')
    success_message = "O evento foi excluído com sucesso."

    def get_context_data(self, **kwargs):
        context = super(EventDeleteView, self).get_context_data(**kwargs)
        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        context['deletable_objects'] = deletable_objects
        context['model_count'] = model_count
        context['protected'] = protected
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(EventDeleteView, self).delete(request, *args, **kwargs)


class EventDetailView(LoginRequiredMixin, EventCreatedByPermission, DetailView):
    model = Event
    template_name = 'core/event/detail.html'


def event_page(request, slug):
    context = {
        'event': Event.objects.get(slug=slug)
    }
    return render(request, 'core/event/public.html', context)
