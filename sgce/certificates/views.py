import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from xhtml2pdf import pisa

from sgce.certificates.forms import TemplateForm, TemplateDuplicateForm, CertificatesCreatorForm, ParticipantForm, \
    CertificateEvaluationForm, CertificateEvaluationTemplateForm
from sgce.certificates.models import Template, Participant, Certificate, CertificateHistory
from sgce.certificates.utils.pdf import link_callback
from sgce.certificates.validators import validate_cpf
from sgce.core.decorators import event_created_by_user_logged_in
from sgce.core.utils.get_deleted_objects import get_deleted_objects


class ParticipantListView(LoginRequiredMixin, ListView):
    model = Participant
    template_name = 'certificates/participant/participant_list.html'
    context_object_name = 'participants'


class ParticipantUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Participant
    form_class = ParticipantForm
    raise_exception = True
    template_name = 'certificates/participant/participant_form.html'
    success_url = reverse_lazy('certificates:participant-list')
    success_message = "O participante %(name)s foi atualizado com sucesso."

    # user_passes_test
    def test_func(self):
        user = self.request.user
        template = self.get_object()
        #Superuser
        if user.is_superuser:
            return True
        return False


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
def template_preview_render_pdf(request, template_pk):
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


@login_required
def certificates_creator(request):
    context = {}

    if request.method == 'POST':
        form = CertificatesCreatorForm(request.user, request.POST, request.FILES)
        context['certificates'] = certificates = request.POST['certificates']
        if form.is_valid():
            certificates_list = []
            template = form.cleaned_data['template']
            for line, attrs_certificate in enumerate(json.loads(certificates), 1):
                if any(attrs_certificate):
                    if (None in attrs_certificate) or ('' in attrs_certificate):
                        messages.error(request, 'A tabela não pode conter valores em branco')
                        certificates_list = False
                        break
                    else:
                        try:
                            attrs_certificate[0] = validate_cpf(attrs_certificate[0])
                        except Exception as e:
                            messages.error(request, 'O CPF {} da linha {} é inválido.'.format(attrs_certificate[0], line))
                            certificates_list = False
                            break

                        certificates_list.append(attrs_certificate)

            if certificates_list:
                inspector = {'certificates': [], 'error': []}
                for attrs in certificates_list:
                    try:
                        certificate = Certificate.objects.create_certificate(template, attrs)
                        inspector['certificates'].append(certificate)
                    except IntegrityError:
                        inspector['error'].append(attrs)

                return render(request, 'certificates/template/inspector.html', {'inspector': inspector})

    else:
        form = CertificatesCreatorForm(request.user)

    context['form'] = form

    return render(request, 'certificates/template/certificates_creator.html', context)


@login_required
def certificates_evaluation(request):
    if request.method == 'POST':
        form = CertificateEvaluationForm(request.user, request.POST)

        if form.is_valid():
            template = form.cleaned_data['template']
            return HttpResponseRedirect(reverse('certificates:certificates-evaluation-template', args=(template.pk,)))

    form = CertificateEvaluationForm(request.user)
    return render(request, 'certificates/template/evaluation.html', {'form': form})


@login_required
@event_created_by_user_logged_in
def certificates_evaluation_template(request, template_pk):
    template = Template.objects.get(pk=template_pk)

    context = {'template': template}

    if request.method == 'POST':
        form = CertificateEvaluationTemplateForm(template_pk, request.POST)
        if form.is_valid():
            notes = form.cleaned_data['notes']
            status = form.cleaned_data['status']
            certificates = form.cleaned_data['certificates']
            for certificate in certificates:
                if certificate.status != status:
                    certificate.status = status
                    certificate.save()
                    CertificateHistory.objects.create(
                        certificate=certificate,
                        user=request.user,
                        notes=notes,
                        ip=request.META.get('REMOTE_ADDR'),
                        status=status,
                    )
            return HttpResponseRedirect(reverse('core:event-detail', args=(template.event.slug,)))
    else:
        form = CertificateEvaluationTemplateForm(template_pk)

    context['form'] = form
    return render(request, 'certificates/template/evaluation_template.html', context)