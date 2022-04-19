# Generated by Django 3.0 on 2020-06-30 20:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0009_auto_20200630_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roommembership',
            name='room',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='roomMemberships', to='space.Room'),
        ),
        migrations.AlterField(
            model_name='spacemembership',
            name='space',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='space.Space'),
        ),
    ]
