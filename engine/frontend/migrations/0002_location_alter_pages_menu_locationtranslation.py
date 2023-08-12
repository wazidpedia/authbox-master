# Generated by Django 4.1.2 on 2022-12-03 10:32

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_cryptography.fields
import parler.fields
import parler.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('menu', '0002_menugroup_kind'),
        ('sites', '0002_alter_domain_unique'),
        ('frontend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('view_count', models.PositiveIntegerField(default=0, editable=False)),
                ('slug', models.SlugField(blank=True, default='', max_length=255, unique=True)),
                ('status', models.SmallIntegerField(choices=[(1, 'Draft'), (2, 'Published')], default=2)),
                ('embed', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='embed')),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sites.site', verbose_name='site')),
            ],
            options={
                'ordering': ['-updated_at'],
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.AlterField(
            model_name='pages',
            name='menu',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='menu.menu', verbose_name='Access From Menu'),
        ),
        migrations.CreateModel(
            name='LocationTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('title', django_cryptography.fields.encrypt(models.CharField(max_length=500, verbose_name='title'))),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='frontend.location')),
            ],
            options={
                'verbose_name': 'location Translation',
                'db_table': 'frontend_location_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
    ]
