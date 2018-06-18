from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from sgce.accounts.models import Profile
from django.contrib.auth import get_user_model


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'perfis'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), UserAdmin)
