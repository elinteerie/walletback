# Generated by Django 5.1.1 on 2024-09-09 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_customuser_address_customuser_city_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={},
        ),
        migrations.AddField(
            model_name='customuser',
            name='username',
            field=models.CharField(default='appuser', max_length=150, unique=True),
        ),
    ]
