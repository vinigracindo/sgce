from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
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


class UserCreateView(SuccessMessageMixin, CreateView):
    model = get_user_model()
    form_class = UserForm
    template_name = 'core/user/user_form.html'
    success_url = reverse_lazy('core:user-list')
    success_message = "O usuário %(username)s foi criado com sucesso."

    # Override form_valid to update user.profile.role
    def form_valid(self, form):
        super(UserCreateView, self).form_valid(form)
        form.instance.profile.role = form.cleaned_data['role']
        form.instance.profile.save()
        return HttpResponseRedirect(self.get_success_url())


class UserUpdateView(SuccessMessageMixin,UpdateView):
    model = get_user_model()
    form_class = UserUpdateForm
    template_name = 'core/user/user_form.html'
    success_url = reverse_lazy('core:user-list')
    success_message = "O usuário %(username)s foi atualizado com sucesso."

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


def user_active_or_disable(request, pk):
    user = get_user_model().objects.get(pk=pk)
    if user.pk is not request.user.pk:
        value = not user.is_active
        user.is_active = value
        user.save()
        messages.success(request, 'O usuário {} foi {} com sucesso.'.format(user.username, 'ativado' if value else 'desativado'))
    else:
        messages.error(request, 'Não é possível desativar o próprio usuário.')
    return HttpResponseRedirect(reverse('core:user-list'))