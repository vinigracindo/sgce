from django.contrib.auth.decorators import login_required
from django.urls import path
from sgce.core import views

app_name = 'core'
urlpatterns = [
    path('', login_required(views.index), name='index'),
    path('user/list/', login_required(views.UserListView.as_view()), name='user-list'),
    path('user/create/', login_required(views.UserCreateView.as_view()), name='user-create'),
    path('user/update/<int:pk>/', login_required(views.UserUpdateView.as_view()), name='user-update'),
    path('user/disable/<int:pk>/', login_required(views.user_active_or_disable), name='user-active-or-disable'),
]