from django.contrib.auth.mixins import UserPassesTestMixin


class TemplateEventCreatedByPermission(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        template = self.get_object()
        #Superuser OR event has been created by yourself.
        if user.is_superuser or template.event.created_by == user:
            return True
        return False