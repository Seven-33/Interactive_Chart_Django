# Generated by Django 3.1.6 on 2021-02-03 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='successful',
            field=models.BooleanField(default=False),
        ),
    ]
