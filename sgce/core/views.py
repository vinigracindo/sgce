from django.shortcuts import render
from django.views.generic import ListView

from sgce.core.models import User


def index(request):
    return render(request, 'core/index.html')


class UserListView(ListView):
    model = User
    template_name = 'core/user_list.html'
    context_object_name = 'users'
