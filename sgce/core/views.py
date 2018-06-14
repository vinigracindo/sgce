from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth import get_user_model

from sgce.core.forms import UserForm, UserUpdateForm


def index(request):
    return render(request, 'core/index.html')


class UserListView(ListView):
    model = get_user_model()
    template_name = 'core/user/user_list.html'
    context_object_name = 'users'


class UserCreateView(CreateView):
    model = get_user_model()
    form_class = UserForm
    template_name = 'core/user/user_form.html'
    success_url = reverse_lazy('core:user-list')

    # Override form_valid to update user.profile.role
    def form_valid(self, form):
        super(UserCreateView, self).form_valid(form)
        form.instance.profile.role = form.cleaned_data['role']
        form.instance.profile.save()
        return HttpResponseRedirect(self.get_success_url())


class UserUpdateView(UpdateView):
    model = get_user_model()
    form_class = UserUpdateForm
    template_name = 'core/user/user_form.html'
    success_url = reverse_lazy('core:user-list')

    def get_initial(self):
        initial = super(UserUpdateView, self).get_initial()
        initial['role'] = self.object.profile.role
        return initial

    # Override form_valid to update user.profile.role
    def form_valid(self, form):
        super(UserUpdateView, self).form_valid(form)
        form.instance.profile.role = form.cleaned_data['role']
        form.instance.profile.save()
        return HttpResponseRedirect(self.get_success_url())