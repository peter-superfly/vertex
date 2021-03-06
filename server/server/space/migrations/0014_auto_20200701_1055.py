# Generated by Django 3.0 on 2020-07-01 10:55

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('space', '0013_auto_20200630_2258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='room_id',
            field=models.CharField(max_length=30, validators=[django.core.validators.RegexValidator(message='Data should be alpha numric.', regex='^\\w+$')]),
        ),
        migrations.AlterField(
            model_name='roommembership',
            name='user',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='roomMembership', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='spacemembership',
            name='user',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='spaceMember', to=settings.AUTH_USER_MODEL),
        ),
    ]
