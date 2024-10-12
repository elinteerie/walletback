# Generated by Django 5.1.1 on 2024-10-12 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_customuser_completed_trades_customuser_rating_trade'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trade',
            name='amount',
        ),
        migrations.AddField(
            model_name='trade',
            name='crypto',
            field=models.CharField(choices=[('spc', 'SPC'), ('tether', 'Tether'), ('btc', 'Bitcoin'), ('eth', 'Ethereum')], default=1, max_length=10),
            preserve_default=False,
        ),
    ]
