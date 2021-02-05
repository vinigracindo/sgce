"""
sgce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name = 'home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name = 'home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.auth import views as auth_views

from sgce.core.views import event_page
from sgce.certificates.views import home

urlpatterns = [
    path('', home, name = 'home'),
    path('event/<slug:slug>/', event_page, name='event-public-page'),
    path('core/', include('sgce.core.urls', namespace = 'core')),
    path('accounts/', include('sgce.accounts.urls', namespace = 'accounts')),
    path('certificates/', include('sgce.certificates.urls', namespace = 'certificates')),
    path(
        'login/',
        auth_views.LoginView.as_view(template_name = 'login.html', redirect_authenticated_user = True),
        name = 'login'
    ),
    path('logout/', auth_views.LogoutView.as_view(next_page = '/login/'), name = 'logout'),
    path('tinymce/', include('tinymce.urls')),
    path('select2/', include('django_select2.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
