# Generated by Django 4.1.2 on 2023-05-14 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0015_fasilities_order_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='order_item',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
