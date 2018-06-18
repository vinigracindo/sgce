from django.db import models
from django.conf import settings


class Profile(models.Model):
    MANAGER = 'm'
    USER = 'u'

    ROLES = (
        (MANAGER, 'Coordenador'),
        (USER, 'Usuário'),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name='usuário',
        on_delete=models.CASCADE
    )
    role = models.CharField('papel', max_length=1, choices=ROLES, default=USER)
    phone = models.CharField('telefone', max_length=16, blank=True)

    class Meta:
        verbose_name = 'perfil'
        verbose_name_plural = 'perfis'
        permissions = (('can_enable_or_disable_user', 'Can change status is_active'),)

    def __str__(self):
        return 'Perfil de {}'.format(self.user.get_full_name())

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #
    #     content_type = ContentType.objects.get_for_model(Profile)
    #     permission = Permission.objects.get(
    #         codename='can_enable_or_disable_user',
    #         content_type=content_type,
    #     )
    #
    #     if self.role == self.MANAGER:
    #         self.user.user_permissions.add(permission)
    #     else:
    #         self.user.user_permissions.remove(permission)