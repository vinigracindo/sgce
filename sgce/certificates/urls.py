from django.urls import path
from sgce.certificates import views

app_name = 'certificates'
urlpatterns = [
    path('template/list/', views.TemplateListView.as_view(), name='template-list'),
]