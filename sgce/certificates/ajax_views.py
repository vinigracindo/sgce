from django.http import JsonResponse
from django.shortcuts import render

from sgce.certificates.models import Template


def ajax_template_header(request, template_pk):
    if request.is_ajax():
        template = Template.objects.get(pk = template_pk)
        data = {
            'headers': template.template_fields()
        }
        return JsonResponse(data)


def load_templates(request):
    if request.is_ajax():
        event_id = request.GET.get('event')
        context = {}
        if event_id:
            templates = Template.objects.filter(event_id = event_id)
        else:
            templates = Template.objects.none()
        return render(request, 'certificates/template/includes/template_dropdown_list_options.html', {'templates': templates})