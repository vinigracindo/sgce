from django.http import JsonResponse

from sgce.certificates.models import Template


def ajax_template_header(request, template_pk):
    if request.is_ajax():
        template = Template.objects.get(pk=template_pk)
        data = {
            'headers': template.template_fields()
        }
        return JsonResponse(data)
