from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name='usuário',
        on_delete=models.CASCADE
    )
    phone = models.CharField('telefone', max_length=16, blank=True)

    class Meta:
        verbose_name = 'perfil'
        verbose_name_plural = 'perfis'

    def __str__(self):
        return 'Perfil de {}'.format(self.user.get_full_name())
