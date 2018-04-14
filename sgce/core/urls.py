from django.urls import path
from sgce.core import views

urlpatterns = [
    path('', views.index, name='index'),
]