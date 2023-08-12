# Generated by Django 4.1.2 on 2023-06-18 05:59

import ckeditor_uploader.fields
from django.db import migrations
import django_cryptography.fields


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0023_photogallery_is_header_text_photogallery_order_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='photogallerytranslation',
            name='content',
            field=django_cryptography.fields.encrypt(ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='content')),
        ),
    ]
