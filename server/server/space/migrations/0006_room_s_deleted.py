# Generated by Django 3.0 on 2020-06-30 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0005_auto_20200630_1839'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='s_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
