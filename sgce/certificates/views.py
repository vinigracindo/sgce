from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from reportlab.lib.styles import getSampleStyleSheet
from xhtml2pdf import pisa

from sgce.certificates.forms import TemplateForm, TemplateDuplicateForm
from sgce.certificates.models import Template
from sgce.certificates.utils.pdf import link_callback
from sgce.core.utils.get_deleted_objects import get_deleted_objects


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


class TemplateDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Template
    raise_exception = True
    template_name = 'certificates/template/template_check_delete.html'
    success_url = reverse_lazy('certificates:template-list')
    success_message = "O modelo foi excluído com sucesso."

    # user_passes_test
    def test_func(self):
        user = self.request.user
        template = self.get_object()
        # Superuser OR template.event has been created by himself.
        if user.is_superuser or template.event.created_by == user:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super(TemplateDeleteView, self).get_context_data(**kwargs)
        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        context['deletable_objects'] = deletable_objects
        context['model_count'] = model_count
        context['protected'] = protected
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(TemplateDeleteView, self).delete(request, *args, **kwargs)


@login_required
def template_duplicate(request, pk):
    template = Template.objects.get(pk=pk)
    if request.method == "POST":
        form = TemplateDuplicateForm(request.user, request.POST)
        if form.is_valid():
            event = form.cleaned_data['event']
            template.pk = None
            template.event = event
            template.save()
            messages.success(request, 'O modelo {} foi duplicado com sucesso.'.format(template))
            return HttpResponseRedirect(reverse('certificates:template-list'))
    else:
        form = TemplateDuplicateForm(request.user)

    context = {
        'form': form,
        'template': template,
    }

    return render(request, 'certificates/template/template_duplicate.html', context)


@login_required
def render_pdf_view(request, template_pk):
    template = Template.objects.get(pk=template_pk)
    template_path = 'certificates/template/pdf/certificate_preview.html'
    context = {'template': template}

    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="{}-{}.pdf"'.format(template.name, 'Modelo Teste')

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)

    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response