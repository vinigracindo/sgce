from django.db import models
from django.utils.text import slugify

from sgce.core.utils.slugify import generate_unique_slug


class Event(models.Model):
    name = models.CharField('nome', max_length=255)
    slug = models.SlugField('slug')
    acronym = models.CharField('sigla', max_length=20)
    start_date = models.DateField('data de início')
    end_date = models.DateField('data de término')
    location = models.CharField('local de realização', max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'evento'
        verbose_name_plural = 'eventos'

    def __str__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return 'core:event-detail', (self.slug,)

    def save(self, *args, **kwargs):
        # Edit
        if self.slug:
            if slugify(self.title) != self.slug:
                self.slug = generate_unique_slug(Event, self.name)
        # Create
        else:
            self.slug = generate_unique_slug(Event, self.name)
        super(Event, self).save(*args, **kwargs)