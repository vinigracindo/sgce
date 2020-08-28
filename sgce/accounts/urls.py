from django.urls import path
from sgce.accounts import views

app_name = 'accounts'
urlpatterns = [
    path('profile/update/', views.ProfileUpdateView.as_view(), name='profile-update'),

    path('user/list/', views.UserListView.as_view(), name='user-list'),
    path('user/create/', views.UserCreateView.as_view(), name='user-create'),
    path('user/update/<int:pk>/', views.UserUpdateView.as_view(), name='user-update'),
    path('user/refresh/access/<int:pk>/', views.user_active_or_disable, name='user-active-or-disable'),
]
