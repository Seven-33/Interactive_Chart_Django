# Generated by Django 3.1.6 on 2021-02-04 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20210205_0038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
