from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth import get_user_model


def index(request):
    return render(request, 'core/index.html')


class UserListView(ListView):
    model = get_user_model()
    template_name = 'core/user_list.html'
    context_object_name = 'users'
