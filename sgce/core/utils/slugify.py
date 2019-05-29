import secrets

from django.utils.text import slugify


def generate_unique_slug(klass, field):
    """
    return unique slug if origin slug is exist.
    eg: `foo-bar` => `foo-bar-1`

    :param `klass` is Class model.
    :param `field` is specific field for title.
    """
    origin_slug = slugify(field)
    unique_slug = origin_slug
    numb = 1
    while klass.objects.filter(slug = unique_slug).exists():
        unique_slug = '%s-%d' % (origin_slug, numb)
        numb += 1
    return unique_slug


def generate_unique_hash(klass, nbytes = 4):
    """
    return unique slug if origin slug is exist.
    eg: `foo-bar` => `foo-bar-1`

    :param `klass` is Class model.
    :param `field` is specific field for title.
    """
    unique_hash = secrets.token_hex(nbytes).upper()

    while klass.objects.filter(hash = unique_hash).exists():
        unique_hash = secrets.token_hex(nbytes).upper()

    return unique_hash
