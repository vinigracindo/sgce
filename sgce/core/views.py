from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth import get_user_model

from sgce.core.forms import UserForm


def index(request):
    return render(request, 'core/index.html')


class UserListView(ListView):
    model = get_user_model()
    template_name = 'core/user/user_list.html'
    context_object_name = 'users'


class UserCreateView(CreateView):
    model = get_user_model()
    form_class = UserForm
    template_name = 'core/user/user_create.html'
    success_url = reverse_lazy('core:user-list')

    def form_valid(self, form):
        super(UserCreateView, self).form_valid(form)
        form.instance.profile.role = form.cleaned_data['role']
        form.instance.profile.save()
        return HttpResponseRedirect(self.get_success_url())