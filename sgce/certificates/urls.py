from django.urls import path
from sgce.certificates import views

app_name = 'certificates'
urlpatterns = [
    path('template/list/', views.TemplateListView.as_view(), name='template-list'),
    path('template/create/', views.TemplateCreateView.as_view(), name='template-create'),
    path('template/update/<int:pk>/', views.TemplateUpdateView.as_view(), name='template-update'),
    path('template/duplicate/<int:pk>/', views.template_duplicate, name='template-duplicate'),
]