# Generated by Django 3.2 on 2021-05-26 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0005_auto_20210525_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='deal',
            name='deliver_to',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='pick_up_from',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
