from django.db import models

from sgce.certificates.validators import validate_cpf


class CertificateManager(models.Manager):
    def create_certificate(self, template, json_attrs):
        cpf, name, *args = json_attrs

        attrs = {}
        fields = template.template_fields()
        for key, value in enumerate(args, 2):
            attrs[fields[key]] = value

        from sgce.certificates.models import Participant
        cpf = validate_cpf(cpf)
        participant, created = Participant.objects.get_or_create(
            cpf=cpf,
            defaults={'name': name}
        )

        certificate = self.create(participant=participant, template=template, fields=str(attrs))

        return certificate
