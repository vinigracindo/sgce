# Generated by Django 2.0.7 on 2018-07-04 21:27

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('certificates', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='backside_content',
            field=tinymce.models.HTMLField(blank=True, verbose_name='texto do verso'),
        ),
        migrations.AlterField(
            model_name='template',
            name='content',
            field=tinymce.models.HTMLField(verbose_name='texto'),
        ),
    ]
