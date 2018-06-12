from django.contrib.auth.decorators import login_required
from django.urls import path
from sgce.core import views

app_name = 'core'
urlpatterns = [
    path('', views.index, name='index'),
    path('user/list/', login_required(views.UserListView.as_view()), name='user-list'),
    path('user/create/', login_required(views.UserCreateView.as_view()), name='user-create'),
]