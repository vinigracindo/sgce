from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from sgce.certificates.forms import TemplateForm
from sgce.certificates.models import Template


class TemplateListView(LoginRequiredMixin, ListView):
    model = Template
    template_name = 'certificates/template/template_list.html'
    context_object_name = 'templates'


class TemplateCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Template
    form_class = TemplateForm
    raise_exception = True
    template_name = 'certificates/template/template_form.html'
    success_url = reverse_lazy('certificates:template-list')
    success_message = "O modelo %(name)s foi criado com sucesso."

    # user_passes_test
    #def test_func(self):
    #    return self.request.user.is_superuser or self.request.user.profile.is_manager()

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        return super(TemplateCreateView, self).form_valid(form)