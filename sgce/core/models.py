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

    def __str__(self):
        return 'Perfil de {}'.format(self.user.get_full_name())