# Generated by Django 4.0.4 on 2023-10-10 20:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='payment',
        ),
    ]
