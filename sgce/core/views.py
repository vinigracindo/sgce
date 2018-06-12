from django.shortcuts import render
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
