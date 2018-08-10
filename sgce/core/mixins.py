from django.contrib.auth.mixins import UserPassesTestMixin


class EventCreatedByPermission(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        event = self.get_object()
        #Superuser OR event has been created by yourself.
        if user.is_superuser or event.created_by == user:
            return True
        return False