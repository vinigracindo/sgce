from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth import get_user_model

from sgce.core.forms import UserForm, UserUpdateForm


@login_required
def index(request):
    return render(request, 'core/index.html')


@login_required
@permission_required('core.can_enable_or_disable_user', raise_exception=True)
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


class UserListView(LoginRequiredMixin, ListView):
    model = get_user_model()
    template_name = 'core/user/user_list.html'
    context_object_name = 'users'


class UserCreateView(LoginRequiredMixin, CreateView, SuccessMessageMixin):
    #permission_required = 'auth.add_user'
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


class UserUpdateView(LoginRequiredMixin, UpdateView, SuccessMessageMixin):
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