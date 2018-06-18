from django.contrib.auth.decorators import login_required
from django.urls import path
from sgce.core import views

app_name = 'core'
urlpatterns = [
    path('', views.index, name='index'),
    path('user/list/', views.UserListView.as_view(), name='user-list'),
    path('user/create/', views.UserCreateView.as_view(), name='user-create'),
    path('user/update/<int:pk>/', views.UserUpdateView.as_view(), name='user-update'),
    path('user/refresh/access/<int:pk>/', views.user_active_or_disable, name='user-active-or-disable'),
]