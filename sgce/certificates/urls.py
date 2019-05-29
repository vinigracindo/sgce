from django.urls import path
from sgce.certificates import views
from sgce.certificates import ajax_views

app_name = 'certificates'
urlpatterns = [
    path('template/list/', views.TemplateListView.as_view(), name = 'template-list'),
    path('template/create/', views.TemplateCreateView.as_view(), name = 'template-create'),
    path('template/update/<int:pk>/', views.TemplateUpdateView.as_view(), name = 'template-update'),
    path('template/duplicate/<int:pk>/', views.template_duplicate, name = 'template-duplicate'),
    path('template/delete/<int:pk>/', views.TemplateDeleteView.as_view(), name = 'template-delete'),
    path('template/preview/<int:template_pk>', views.template_preview_render_pdf, name = 'template-pdf-preview'),
    path('ajax/load/templates/', ajax_views.load_templates, name = 'ajax_load_templates'),

    path('certificate/pdf/<str:hash>/', views.certificate_render_pdf, name = 'certificate-pdf'),
    path('certificates/creator/', views.certificates_creator, name = 'certificates-creator'),
    path('certificates/ajax/template/header/<int:template_pk>/', ajax_views.ajax_template_header, name = 'ajax_template_header'),
    path('certificates/evaluation/', views.certificates_evaluation, name = 'certificates-evaluation'),
    path('certificate/evaluation/<int:template_pk>/', views.certificates_evaluation_template, name = 'certificates-evaluation-template'),
    path('certificate/validate/', views.certificate_validate, name = 'certificate-validate'),
    path('certificate/list/', views.CertificateListView.as_view(), name = 'certificate-list'),
    path('certificate/<str:hash>/', views.certificate_detail, name = 'certificate-detail'),
    path('certificate/history/<int:certificate_pk>/', views.certificate_history, name = 'certificate-history'),

    path('participant/list/', views.ParticipantListView.as_view(), name = 'participant-list'),
    path('participant/update/<int:pk>/', views.ParticipantUpdateView.as_view(), name = 'participant-update'),
]