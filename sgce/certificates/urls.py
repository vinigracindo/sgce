from django.urls import path
from sgce.certificates import views

app_name = 'certificates'
urlpatterns = [
    path('template/list/', views.TemplateListView.as_view(), name='template-list'),
    path('template/create/', views.TemplateCreateView.as_view(), name='template-create'),
    path('template/update/<int:pk>/', views.TemplateUpdateView.as_view(), name='template-update'),
    path('template/duplicate/<int:pk>/', views.template_duplicate, name='template-duplicate'),
    path('template/delete/<int:pk>/', views.TemplateDeleteView.as_view(), name='template-delete'),
    path('template/preview/<int:template_pk>', views.render_pdf_view, name='template-pdf-preview')
]