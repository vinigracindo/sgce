import re

from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator
from jsonfield import JSONField
from tinymce.models import HTMLField

from sgce.certificates.validators import validate_cpf
from sgce.core.models import Event
from sgce.core.utils.list import remove_duplicates
from sgce.core.utils.slugify import generate_unique_hash


class Template(models.Model):
    ARIAL = 'arial'
    TIMES_NEW_ROMAN = 'times'
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
        related_name='templates',
        on_delete=models.PROTECT
    )
    title = models.CharField('título', max_length=64, blank=True)
    content = HTMLField(
        'texto',
        default='''
        Exemplo: Certificamos que NOME_COMPLETO participou do evento NOME_EVENTO, realizado em DATA_EVENTO.
        ''',
        help_text='''
        O arquivo importado deve estar no formato CSV, com a separação dos campos por ponto-e-vírgula (;) e ter, 
        obrigatoriamente, o campo NUMERO_CPF e NOME_COMPLETO. Poderá também conter outros campos, desde que formados 
        por duas palavras maiúsculas separadas pelo caractere sublinhado (underline), como no texto 
        de exemplo. Evite usar o ponto-e-vírgula junto ao nome de um campo dentro do texto do certificado para evitar 
        problemas na importação de dados.
        '''
    )
    backside_title = models.CharField('título do verso', max_length=64, blank=True)
    backside_content = HTMLField('texto do verso', blank=True)
    background = models.ImageField(
        verbose_name='imagem de fundo',
        upload_to='backgrounds',
        blank=True,
        help_text='''
        É recomendado que imagem de fundo deverá ter 3508 pixels de largura e 2480 pixels de altura, 
        correspondendo a uma folha A4 na orientação de paisagem.
        '''
    )
    font = models.CharField('fonte', max_length=10, choices=FONTS, default=ARIAL)
    title_top_distance = models.PositiveIntegerField(
        'distância do topo ao título',
        blank=True,
        default=3,
        validators=[MaxValueValidator(10)]
    )
    title_section_align = models.CharField(
        'alinhamento da seção',
        max_length=10,
        choices=SECTION_ALIGN,
        default=CENTER
    )
    title_align = models.CharField(
        'alinhamento do título',
        max_length=10,
        choices=TEXT_ALIGN,
        default=CENTER
    )
    title_color = models.CharField('cor do título', max_length=10, choices=COLOR, default=BLACK)
    title_font_size = models.PositiveIntegerField('tamanho da fonte do título', default=30)
    content_title_distance = models.PositiveIntegerField(
        'distância do título ao texto',
        blank=True,
        default=1,
        validators=[MaxValueValidator(10)]
    )
    content_section_align = models.CharField(
        'alinhamento da seção',
        max_length=10,
        choices=SECTION_ALIGN,
        default=CENTER
    )
    content_text_align = models.CharField(
        'alinhmento do texto',
        max_length=10,
        choices=TEXT_ALIGN,
        default=JUSTIFY
    )
    content_text_color = models.CharField('cor do texto', max_length=10, choices=COLOR, default=BLACK)
    content_font_size = models.PositiveIntegerField('tamanho da fonte do texto', default=12)
    footer_title_distance = models.PositiveIntegerField(
        'distância do texto ao rodapé',
        blank=True,
        default=0,
        validators=[MaxValueValidator(10)]
    )
    footer_section_align = models.CharField(
        'alinhamento da seção',
        blank=True,
        max_length=10,
        choices=SECTION_ALIGN,
        default=CENTER
    )
    footer_text_align = models.CharField(
        'alinhamento do rodapé',
        max_length=10,
        choices=TEXT_ALIGN,
        default=CENTER
    )
    footer_text_color = models.CharField('cor do rodapé', max_length=10, choices=COLOR, default=BLACK)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'modelo'
        ordering = ['-created_at']

    def __str__(self):
        return '{}: {}'.format(self.event, self.name)

    def template_fields(self):
        """Must return the fields that will build the certificate. The pattern: UPPERCASE_UPPERCASE"""
        required_fields = ['NUMERO_CPF', 'NOME_COMPLETO']
        another_fields = re.findall(r'\b([A-Z]+_[A-Z]+)\b', self.content)
        return remove_duplicates(required_fields + another_fields)


class Participant(models.Model):
    cpf = models.CharField(max_length=11, unique=True, validators=[validate_cpf])
    email = models.EmailField(blank=True)
    name = models.CharField('nome', max_length=128)

    class Meta:
        verbose_name = 'participante'

    def __str__(self):
        cpf = '{}.{}.{}-{}'.format(self.cpf[:3], self.cpf[3:6], self.cpf[6:9], self.cpf[9:])
        return '{} ({})'.format(self.name, cpf)


class Certificate(models.Model):
    PENDING = 'p'
    VALID = 'v'
    REVOKED = 'r'
    STATUS_CHOICES = (
        (PENDING, 'Pendente'),
        (VALID, 'Válido'),
        (REVOKED, 'Revogado'),
    )
    participant = models.ForeignKey(
        Participant,
        verbose_name='participante',
        related_name='certificates',
        on_delete=models.PROTECT,
    )
    template = models.ForeignKey(
        Template,
        verbose_name='modelo',
        related_name='certificates',
        on_delete=models.PROTECT,
    )
    hash = models.CharField(max_length=255, editable=False)
    fields = JSONField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PENDING)

    class Meta:
        verbose_name = 'certificado'
        unique_together = ('participant', 'template', 'fields')

    def __str__(self):
        return 'Certificado de {} do modelo {}'.format(self.participant.name, self.template.name)

    def save(self, *args, **kwargs):
        if not self.hash:
            self.hash = generate_unique_hash(Certificate)
        super(Certificate, self).save(*args, **kwargs)


class CertificateHistory(models.Model):
    certificate = models.ForeignKey(
        Certificate,
        verbose_name='certificado',
        related_name='logs',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='usuário',
        on_delete=models.CASCADE
    )
    notes = models.TextField('observação', blank=True)
    ip = models.GenericIPAddressField(protocol='IPv4')
    status = models.CharField(max_length=1, choices=Certificate.STATUS_CHOICES)
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'histórico'

    def __str__(self):
        return '{} - {}'.format(self.certificate, self.user)