from django.core.exceptions import PermissionDenied
from sgce.certificates.models import Template, Certificate


def template_event_created_by_user_logged_in_required(function):
    def wrap(request, *args, **kwargs):
        entry = Template.objects.get(pk = kwargs['template_pk'])
        if request.user.is_superuser or entry.event.created_by == request.user:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def certificate_event_created_by_user_logged_in_required(function):
    def wrap(request, *args, **kwargs):
        entry = Certificate.objects.get(pk = kwargs['certificate_pk'])
        if request.user.is_superuser or entry.template.event.created_by == request.user:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap