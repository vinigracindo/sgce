import json

from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.validators import validate_email
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import get_template
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.conf import settings
from sgce.core.utils.ip import get_client_ip
from xhtml2pdf import pisa

from sgce.certificates.forms import TemplateForm, TemplateDuplicateForm, CertificatesCreatorForm, ParticipantForm, \
    CertificateEvaluationForm, CertificateEvaluationTemplateForm, HomeForm, CertificateValidateForm
from sgce.certificates.mixins import TemplateEventCreatedByPermission
from sgce.certificates.models import Template, Participant, Certificate, CertificateHistory
from sgce.certificates.utils.pdf import link_callback
from sgce.certificates.validators import validate_cpf
from sgce.core.decorators import template_event_created_by_user_logged_in_required, \
    certificate_event_created_by_user_logged_in_required
from sgce.core.utils.get_deleted_objects import get_deleted_objects


def home(request):
    context = {}
    if request.method == 'POST':
        form = HomeForm(request.POST)
        if form.is_valid():
            cpf = form.cleaned_data['cpf']

            certificates = Certificate.objects\
                .filter(participant__cpf=cpf, status=Certificate.VALID)\
                .order_by('-created_at')\
                .select_related()

            if certificates.exists():
                context['certificates'] = certificates
            else:
                messages.error(
                    request, 'Não existem certificados válidos para este CPF.')
    else:
        form = HomeForm()
    context['form'] = form
    return render(request, 'home.html', context)


def certificate_validate(request):
    context = {}
    if request.method == 'POST':
        form = CertificateValidateForm(request.POST)
        if form.is_valid():
            hash = form.cleaned_data['hash']
            return redirect('certificates:certificate-detail', hash=hash)

    else:
        form = CertificateValidateForm()
    context['form'] = form
    return render(request, 'certificates/certificate/validate.html', context)


def certificate_detail(request, hash):
    context = {}
    try:
        context['certificate'] = Certificate.objects.get(hash=hash)
    except Certificate.DoesNotExist:
        pass

    return render(request, 'certificates/certificate/detail.html', context)


class ParticipantListView(LoginRequiredMixin, ListView):
    model = Participant
    raise_exception = True
    template_name = 'certificates/participant/list.html'
    context_object_name = 'participants'


class ParticipantUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Participant
    form_class = ParticipantForm
    raise_exception = True
    template_name = 'certificates/participant/form.html'
    success_url = reverse_lazy('certificates:participant-list')
    success_message = "O participante %(name)s foi atualizado com sucesso."

    # user_passes_test
    def test_func(self):
        return self.request.user.is_superuser


class TemplateListView(LoginRequiredMixin, ListView):
    model = Template
    template_name = 'certificates/template/list.html'
    context_object_name = 'templates'

    def get_queryset(self):
        # Show all publics template and all templates created by logged user
        return Template.objects.filter(Q(event__created_by=self.request.user) | Q(is_public=True)).distinct()


class TemplateCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Template
    form_class = TemplateForm
    permission_required = 'certificates.add_template'
    raise_exception = True
    template_name = 'certificates/template/form.html'
    success_url = reverse_lazy('certificates:template-list')
    success_message = "O modelo %(name)s foi criado com sucesso."


class TemplateUpdateView(LoginRequiredMixin, TemplateEventCreatedByPermission, SuccessMessageMixin, UpdateView):
    model = Template
    form_class = TemplateForm
    template_name = 'certificates/template/form.html'
    success_url = reverse_lazy('certificates:template-list')
    success_message = "O modelo %(name)s foi atualizado com sucesso."


class TemplateDeleteView(LoginRequiredMixin, TemplateEventCreatedByPermission, DeleteView):
    model = Template
    template_name = 'certificates/template/delete.html'
    success_url = reverse_lazy('certificates:template-list')
    success_message = "O modelo foi excluído com sucesso."

    def get_context_data(self, **kwargs):
        context = super(TemplateDeleteView, self).get_context_data(**kwargs)
        deletable_objects, model_count, protected = get_deleted_objects([
                                                                        self.object])
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
            messages.success(
                request, 'O modelo {} foi duplicado com sucesso.'.format(template))
            return HttpResponseRedirect(reverse('certificates:template-list'))
    else:
        form = TemplateDuplicateForm(request.user)

    context = {
        'form': form,
        'template': template,
    }

    return render(request, 'certificates/template/duplicate.html', context)


@login_required
def template_preview_render_pdf(request, template_pk):
    template = Template.objects.get(pk=template_pk)
    template_path = 'certificates/template/pdf/preview.html'
    context = {'template': template, 'domain': settings.SITE_URL}

    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="{}-{}.pdf"'.format(
        template.id, 'Modelo Teste')

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback)

    # if error then show some view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response


def certificate_render_pdf(request, hash):
    certificate = get_object_or_404(Certificate, hash=hash)
    template_path = 'certificates/certificate/pdf/certificate.html'

    context = {'certificate': certificate, 'domain': settings.SITE_URL}

    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="certificado.pdf"'

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback)

    # if error then show some view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response


@login_required
def certificates_creator(request):
    context = {}

    if request.method == 'POST':
        form = CertificatesCreatorForm(
            request.user, request.POST, request.FILES)
        context['certificates'] = request.POST['certificates']

        if form.is_valid():
            template = form.cleaned_data['template']
            certificates = form.cleaned_data['certificates']

            certificates = json.loads(certificates)

            inspector = {'certificates': [], 'error': []}

            for certificate_attrs in certificates:
                cpf, name, *args = [x.strip() for x in certificate_attrs]
                attrs = {}

                for key, value in enumerate(args, 2):
                    attrs[template.template_fields()[key]] = value

                participant, created = Participant.objects.get_or_create(
                    cpf=validate_cpf(cpf),
                    defaults={'name': name}
                )

                try:
                    certificate = Certificate.objects.create(
                        participant=participant, template=template, fields=attrs)
                    inspector['certificates'].append(certificate)
                except IntegrityError:
                    inspector['error'].append(certificate_attrs)

            return render(request, 'certificates/template/inspector.html', {'inspector': inspector})

    else:
        form = CertificatesCreatorForm(request.user)

    context['form'] = form

    return render(request, 'certificates/certificate/generator.html', context)


@login_required
@certificate_event_created_by_user_logged_in_required
def certificate_history(request, certificate_pk):
    certificate = get_object_or_404(Certificate, pk=certificate_pk)
    return render(request, 'certificates/certificate/history.html', {'certificate': certificate})


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
@template_event_created_by_user_logged_in_required
def certificates_evaluation_template(request, template_pk):
    template = Template.objects.get(pk=template_pk)

    context = {'template': template}

    if request.method == 'POST':
        form = CertificateEvaluationTemplateForm(template_pk, request.POST)
        if form.is_valid():
            notes = form.cleaned_data['notes']
            status = form.cleaned_data['status']
            certificates = form.cleaned_data['certificates']

            certificates = certificates.exclude(status=status)

            for certificate in certificates:
                CertificateHistory.objects.create(
                    certificate=certificate,
                    user=request.user,
                    notes=notes,
                    ip=get_client_ip(request),
                    status=status,
                )

            certificates.update(status=status)

            return HttpResponseRedirect(reverse('core:event-detail', args=(template.event.slug,)))
    else:
        form = CertificateEvaluationTemplateForm(template_pk)

    context['form'] = form
    return render(request, 'certificates/template/evaluation_template.html', context)


class CertificateListView(LoginRequiredMixin, ListView):
    model = Certificate
    raise_exception = True
    template_name = 'certificates/certificate/list.html'
    context_object_name = 'certificates'

    def get_queryset(self):
        queryset = super(CertificateListView, self).get_queryset()
        user = self.request.user
        return queryset if user.is_superuser else queryset.filter(template__event__created_by=self.request.user)
