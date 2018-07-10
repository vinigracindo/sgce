from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from sgce.certificates.forms import TemplateForm
from sgce.certificates.models import Template


class TemplateListView(LoginRequiredMixin, ListView):
    model = Template
    template_name = 'certificates/template/template_list.html'
    context_object_name = 'templates'


class TemplateCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Template
    form_class = TemplateForm
    permission_required = 'certificates.add_template'
    raise_exception = True
    template_name = 'certificates/template/template_form.html'
    success_url = reverse_lazy('certificates:template-list')
    success_message = "O modelo %(name)s foi criado com sucesso."


class TemplateUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Template
    form_class = TemplateForm
    raise_exception = True
    template_name = 'certificates/template/template_form.html'
    success_url = reverse_lazy('certificates:template-list')
    success_message = "O modelo %(name)s foi atualizado com sucesso."

    # user_passes_test
    def test_func(self):
        user = self.request.user
        template = self.get_object()
        #Superuser OR template.event has been created by himself.
        if user.is_superuser or template.event.created_by == user:
            return True
        return False
