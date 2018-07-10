from django.db import models
from django.conf import settings
import re

from tinymce.models import HTMLField

from sgce.core.models import Event


class Template(models.Model):
    ARIAL = 'a'
    TIMES_NEW_ROMAN = 't'
    FONTS = (
        (ARIAL, 'Arial'),
        (TIMES_NEW_ROMAN, 'Times New Roman')
    )
    LEFT = 'left'
    CENTER = 'center'
    RIGHT = 'right'
    JUSTIFY = 'justify'
    SECTION_ALIGN = (
        (LEFT, 'Alinhar seção à esquerda'),
        (CENTER, 'Seção centralizada'),
        (RIGHT, 'Alinhar seção à direita'),
    )
    TEXT_ALIGN = (
        (LEFT, 'Alinhar texto à esquerda'),
        (CENTER, 'Texto centralizado'),
        (RIGHT, 'Alinhar texto à direita'),
        (JUSTIFY, 'Texto justificado'),
    )
    BLACK = '#000'
    WHITE = '#FFF'
    LIGHT_GRAY = '#CCC'
    DARK_GRAY = '#999'
    COLOR = (
        (BLACK, 'Preto'),
        (WHITE, 'Preto'),
        (LIGHT_GRAY, 'Cinza claro'),
        (DARK_GRAY, 'Cinza escuro'),
    )
    name = models.CharField('nome', max_length=64)
    event = models.ForeignKey(
        Event,
        verbose_name='evento',
        on_delete=models.PROTECT
    )
    title = models.CharField('título', max_length=64, blank=True)
    content = HTMLField('texto')
    backside_title = models.CharField('título do verso', max_length=64, blank=True)
    backside_content = HTMLField('texto do verso', blank=True)
    background = models.ImageField(
        verbose_name='imagem de fundo',
        upload_to='backgrounds',
        blank=True,
        help_text='''
        A imagem de fundo deverá ter 3508 pixels de largura e 2480 pixels de altura, correspondendo a uma 
        folha A4 na orientação de paisagem.
        '''
    )
    font = models.CharField('fonte', max_length=1, choices=FONTS, default=ARIAL)
    title_top_distance = models.PositiveIntegerField('distância do topo ao título', blank=True, default=0)
    title_section_align = models.CharField(
        'alinhamento da seção',
        max_length=10,
        choices=SECTION_ALIGN,
        default=LEFT
    )
    title_align = models.CharField(
        'alinhamento do título',
        max_length=10,
        choices=TEXT_ALIGN,
        default=LEFT
    )
    title_color = models.CharField('cor do título', max_length=10, choices=COLOR, default=BLACK)
    title_font_size = models.PositiveIntegerField('tamanho da fonte do título', default=30)
    content_title_distance = models.PositiveIntegerField('distância do título ao texto', blank=True, default=0)
    content_section_align = models.CharField(
        'alinhamento da seção',
        max_length=10,
        choices=SECTION_ALIGN,
        default=LEFT
    )
    content_text_align = models.CharField(
        'alinhmento do texto',
        max_length=10,
        choices=TEXT_ALIGN,
        default=LEFT
    )
    content_text_color = models.CharField('cor do texto', max_length=10, choices=COLOR, default=BLACK)
    content_font_size = models.PositiveIntegerField('tamanho da fonte do texto', default=12)
    footer_title_distance = models.PositiveIntegerField('distância do texto ao rodapé', blank=True, default=0)
    footer_section_align = models.CharField(
        'alinhamento da seção',
        blank=True,
        max_length=10,
        choices=SECTION_ALIGN,
        default=LEFT
    )
    footer_text_align = models.CharField(
        'alinhamento do rodapé',
        max_length=10,
        choices=TEXT_ALIGN,
        default=LEFT
    )
    footer_text_color = models.CharField('cor do rodapé', max_length=10, choices=COLOR, default=BLACK)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}: {}'.format(self.event, self.name)

    def template_fields(self):
        """Must return the fields that will build the certificate. The pattern: UPPERCASE_UPPERCASE"""
        return re.findall(r'\b([A-Z]+_[A-Z]+)\b', self.content)