# Generated by Django 4.0.4 on 2023-06-18 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='quantity',
            new_name='total',
        ),
    ]
