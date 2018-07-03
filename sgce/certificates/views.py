from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView

from sgce.certificates.models import Template


class TemplateListView(LoginRequiredMixin, ListView):
    model = Template
    template_name = 'certificates/template/template_list.html'
    context_object_name = 'templates'