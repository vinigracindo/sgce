from django.urls import path
from sgce.core import views

app_name = 'core'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('event/list/', views.EventListView.as_view(), name = 'event-list'),
    path('event/create/', views.EventCreateView.as_view(), name = 'event-create'),
    path('event/update/<int:pk>/', views.EventUpdateView.as_view(), name = 'event-update'),
    path('event/delete/<int:pk>/', views.EventDeleteView.as_view(), name = 'event-delete'),
    path('event/<slug:slug>/', views.EventDetailView.as_view(), name = 'event-detail'),
]