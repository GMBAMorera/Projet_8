# Generated by Django 3.1.7 on 2021-03-11 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20210303_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='aliment',
            name='image',
            field=models.CharField(default=None, max_length=256),
            preserve_default=False,
        ),
    ]
