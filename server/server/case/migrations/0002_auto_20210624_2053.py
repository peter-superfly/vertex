# Generated by Django 3.0 on 2021-06-24 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('case', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='kenyalaw_id',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='case',
            name='case_action',
            field=models.CharField(choices=[('Revision', 'Revision'), ('Judgment', 'Judgment'), ('Ruling', 'Ruling')], max_length=10),
        ),
        migrations.AlterField(
            model_name='case',
            name='case_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
