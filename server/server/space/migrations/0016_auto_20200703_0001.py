# Generated by Django 3.0 on 2020-07-03 00:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0015_auto_20200702_2359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spacemembership',
            name='space',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='spaceMemberships', to='space.Space'),
        ),
    ]
