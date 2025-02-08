# Generated by Django 2.1 on 2021-01-06 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crashdiagramorientation',
            name='movement_code',
            field=models.CharField(blank=True, error_messages={'unique': 'A movement_code already exists.'}, max_length=65, null=True, unique=True),
        ),
    ]
