# Generated by Django 4.2.4 on 2023-08-10 14:15

from django.db import migrations
import django_ckeditor_5.fields
import django_cryptography.fields


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0028_alter_heroimagetranslation_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aboutustranslation',
            name='content',
            field=django_cryptography.fields.encrypt(django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='content')),
        ),
        migrations.AlterField(
            model_name='announcementtranslation',
            name='content',
            field=django_cryptography.fields.encrypt(django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='content')),
        ),
        migrations.AlterField(
            model_name='articletranslation',
            name='content',
            field=django_cryptography.fields.encrypt(django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='content')),
        ),
        migrations.AlterField(
            model_name='documenttranslation',
            name='content',
            field=django_cryptography.fields.encrypt(django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='content')),
        ),
        migrations.AlterField(
            model_name='eventstranslation',
            name='content',
            field=django_cryptography.fields.encrypt(django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='content')),
        ),
        migrations.AlterField(
            model_name='fasilitiestranslation',
            name='content',
            field=django_cryptography.fields.encrypt(django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='content')),
        ),
        migrations.AlterField(
            model_name='greetingtranslation',
            name='content',
            field=django_cryptography.fields.encrypt(django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='content')),
        ),
        migrations.AlterField(
            model_name='location',
            name='embed',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='embed'),
        ),
        migrations.AlterField(
            model_name='newstranslation',
            name='content',
            field=django_cryptography.fields.encrypt(django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='content')),
        ),
        migrations.AlterField(
            model_name='offerstranslation',
            name='content',
            field=django_cryptography.fields.encrypt(django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='content')),
        ),
        migrations.AlterField(
            model_name='pagestranslation',
            name='content',
            field=django_cryptography.fields.encrypt(django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='content')),
        ),
        migrations.AlterField(
            model_name='photogallerytranslation',
            name='content',
            field=django_cryptography.fields.encrypt(django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='content')),
        ),
        migrations.AlterField(
            model_name='producttranslation',
            name='content',
            field=django_cryptography.fields.encrypt(django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='content')),
        ),
        migrations.AlterField(
            model_name='slideshowtranslation',
            name='content',
            field=django_cryptography.fields.encrypt(django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='content')),
        ),
        migrations.AlterField(
            model_name='videogallery',
            name='embed',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='embed'),
        ),
    ]
