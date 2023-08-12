# Generated by Django 4.1.2 on 2022-12-03 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0002_location_alter_pages_menu_locationtranslation'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='status',
            field=models.SmallIntegerField(choices=[(1, 'Draft'), (2, 'Published')], default=2),
        ),
        migrations.AddField(
            model_name='tags',
            name='status',
            field=models.SmallIntegerField(choices=[(1, 'Draft'), (2, 'Published')], default=2),
        ),
    ]