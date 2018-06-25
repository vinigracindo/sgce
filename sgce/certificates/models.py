from django.db import models
from django.conf import settings
from sgce.core.models import Event


class Template(models.Model):
    name = models.CharField('nome', max_length=64)
    event = models.ForeignKey(
        Event,
        verbose_name='evento',
        on_delete=models.PROTECT
    )
    title = models.CharField('título', max_length=64, blank=True)
    content = models.TextField('texto')
    backside_title = models.CharField('título do verso', max_length=64, blank=True)
    backside_content = models.TextField('texto do verso', blank=True)
    background = models.ImageField(
        verbose_name='imagem de fundo',
        upload_to='backgrounds',
        blank=True,
        help_text='''
        A imagem de fundo deverá ter 3508 pixels de largura e 2480 pixels de altura, correspondendo a uma 
        folha A4 na orientação de paisagem.
        '''
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='criado por',
        on_delete=models.PROTECT,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name