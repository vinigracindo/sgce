from django.urls import path
from sgce.core import views

app_name = 'core'
urlpatterns = [
    path('', views.index, name='index'),
    path('event/<slug:slug>/', views.event_detail, name='event-detail'),
]