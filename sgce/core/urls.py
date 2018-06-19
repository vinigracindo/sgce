from django.urls import path
from sgce.core import views

app_name = 'core'
urlpatterns = [
    path('', views.index, name='index'),
    path('event/list/', views.EventListView.as_view(), name='event-list'),
    path('event/create/', views.EventCreateView.as_view(), name='event-create'),
    path('event/<slug:slug>/', views.event_detail, name='event-detail'),
]