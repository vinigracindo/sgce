from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.conf import settings
from sgce.core.utils.slugify import generate_unique_slug


class Event(models.Model):
    name = models.CharField('nome', max_length=255)
    slug = models.SlugField('slug', unique=True, editable=False, max_length=300)
    start_date = models.DateField('data de início')
    end_date = models.DateField('data de término')
    location = models.CharField('local de realização', max_length=255, blank=True)
    has_public_page = models.BooleanField(
        'Criar uma página pública',
        help_text=
        '''
        Cria uma página pública do evento que mostra todos os certificados.
        Recomenda-se não marcar essa opção caso o certificado possua dados sensíveis
        como CPF.
        ''',
        default=False,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='criado por',
        related_name='events',
        on_delete=models.PROTECT,
    )
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        verbose_name = 'evento'
        verbose_name_plural = 'eventos'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('core:event-detail', args = [self.slug])

    def save(self, *args, **kwargs):
        # Edit
        if self.slug:
            if slugify(self.name) != self.slug:
                self.slug = generate_unique_slug(Event, self.name)
        # Create
        else:
            self.slug = generate_unique_slug(Event, self.name)
        super(Event, self).save(*args, **kwargs)