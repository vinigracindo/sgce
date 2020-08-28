import re

from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from django.utils.safestring import mark_safe
from jsonfield import JSONField
from tinymce.models import HTMLField

from sgce.certificates.utils.text import remove_accents
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
    name = models.CharField('nome', max_length=255)
    event = models.ForeignKey(
        Event,
        verbose_name='evento',
        related_name='templates',
        on_delete=models.PROTECT
    )
    title = models.CharField('título', max_length=255, blank=True)
    content = HTMLField(
        'texto',
        default='''
        Exemplo: Certificamos que NOME_COMPLETO participou do evento NOME_EVENTO, realizado em DATA_EVENTO.
        ''',
        help_text='''
        Os campos que compõem o certificado devem ser formados por duas palavras maísculas separadas pelo
        caractere sublinhado (underline), como no texto de exemplo:
        Certificamos que NOME_COMPLETO participou do evento NOME_EVENTO, realizado em DATA_EVENTO
        '''
    )
    backside_title = models.CharField('título do verso', max_length=255, blank=True)
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
    title_top_distance = models.DecimalField(
        'distância do topo ao título',
        decimal_places=1,
        max_digits=2,
        default=3,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
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
    title_color = models.CharField('cor do título', max_length = 10, choices = COLOR, default = BLACK)
    title_font_size = models.PositiveIntegerField('tamanho da fonte do título', default = 30)
    content_title_distance = models.DecimalField(
        'distância do título ao texto',
        decimal_places=1,
        max_digits=2,
        default=1.0,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
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
    footer_title_distance = models.DecimalField(
        'distância do texto ao rodapé',
        decimal_places=1,
        max_digits=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    footer_section_align = models.CharField(
        'alinhamento da seção',
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
    has_qrcode = models.BooleanField(verbose_name='tem qrcode?', default=True)
    is_public = models.BooleanField(verbose_name='É público?', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'modelo'
        ordering = ['-created_at']

    def __str__(self):
        return '{}: {}'.format(self.event, self.name)

    def template_fields(self):
        """Must return the fields that will build the certificate. The pattern: UPPERCASE_UPPERCASE"""
        #optional_field = ['ENDERECO_EMAIL']
        required_fields = ['NUMERO_CPF', 'NOME_COMPLETO']
        another_fields = re.findall(r'\b([A-Z]+_[A-Z]+)\b', remove_accents(self.content))
        #return remove_duplicates(optional_field + required_fields + another_fields)
        return remove_duplicates(required_fields + another_fields)


class Participant(models.Model):
    cpf = models.CharField(max_length = 11, unique = True, validators = [validate_cpf])
    email = models.EmailField(blank = True)
    name = models.CharField('nome', max_length = 128)

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
        verbose_name = 'participante',
        related_name = 'certificates',
        on_delete = models.PROTECT,
    )
    template = models.ForeignKey(
        Template,
        verbose_name = 'modelo',
        related_name = 'certificates',
        on_delete = models.PROTECT,
    )
    hash = models.CharField(max_length = 255, editable = False, unique = True)
    fields = JSONField()
    status = models.CharField(max_length = 1, choices = STATUS_CHOICES, default = PENDING)
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        verbose_name = 'certificado'
        unique_together = ('participant', 'template', 'fields')

    def __str__(self):
        return 'Certificado de {} do modelo {}'.format(self.participant.name, self.template.name)

    def get_absolute_url(self):
        return reverse('certificates:certificate-detail', args = [self.hash])

    def save(self, *args, **kwargs):
        if not self.hash:
            self.hash = generate_unique_hash(Certificate)
        super(Certificate, self).save(*args, **kwargs)

    def get_safe_content(self):
        content = self.template.content
        content = content.replace('NOME_COMPLETO', self.participant.name).replace('NUMERO_CPF', self.participant.cpf)

        for key in self.fields:
            content = content.replace(key, self.fields[key])

        return mark_safe(content)

    def is_valid(self):
        return True if self.status == Certificate.VALID else False


class CertificateHistory(models.Model):
    certificate = models.ForeignKey(
        Certificate,
        verbose_name = 'certificado',
        related_name = 'logs',
        on_delete = models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name = 'usuário',
        on_delete = models.CASCADE
    )
    notes = models.TextField('observação', blank = True)
    ip = models.GenericIPAddressField(protocol = 'IPv4')
    status = models.CharField(max_length = 1, choices = Certificate.STATUS_CHOICES)
    datetime = models.DateTimeField(auto_now_add = True)

    class Meta:
        verbose_name = 'histórico'
        ordering = ['-datetime']

    def __str__(self):
        return '{} - {}'.format(self.certificate, self.user)