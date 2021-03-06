# Generated by Django 3.0 on 2020-06-16 06:25

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('display_name', models.CharField(max_length=100)),
                ('description', models.CharField(default='', max_length=500)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('display_name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=128, null=True)),
                ('thumb_url', models.CharField(max_length=128, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_private', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='RoomMembership',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('invite_time_first', models.DateTimeField(default=django.utils.timezone.now)),
                ('invite_time_last', models.DateTimeField(default=django.utils.timezone.now)),
                ('join_time', models.DateTimeField(null=True)),
                ('deactivate_time', models.DateTimeField(null=True)),
                ('membership_status', models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive'), ('INVITED', 'Invited'), ('DECLINED', 'Decline')], default='INACTIVE', max_length=8)),
                ('membership_type', models.CharField(choices=[('ADMIN', 'Admin'), ('MEMBER', 'Member'), ('GUEST', 'Guest')], default='MEMBER', max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='Space',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('space_name', models.CharField(max_length=24, unique=True)),
                ('display_name', models.CharField(max_length=32)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_private', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SpaceMemberShip',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('invite_time_first', models.DateTimeField(default=django.utils.timezone.now)),
                ('invite_time_last', models.DateTimeField(default=django.utils.timezone.now)),
                ('join_time', models.DateTimeField(null=True)),
                ('deactivate_time', models.DateTimeField(null=True)),
                ('membership_status', models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive'), ('INVITED', 'Invited'), ('DECLINED', 'Decline')], default='INACTIVE', max_length=8)),
                ('membership_type', models.CharField(choices=[('ADMIN', 'Admin'), ('MEMBER', 'Member'), ('GUEST', 'Guest')], default='MEMBER', max_length=8)),
            ],
        ),
    ]
