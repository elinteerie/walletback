# Generated by Django 5.1.1 on 2024-09-09 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_transaction_success'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='success',
        ),
    ]
