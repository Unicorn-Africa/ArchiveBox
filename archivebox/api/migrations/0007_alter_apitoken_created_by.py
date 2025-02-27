# Generated by Django 5.1 on 2024-08-20 22:52

import abid_utils.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_remove_outboundwebhook_uuid_apitoken_id_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='apitoken',
            name='created_by',
            field=models.ForeignKey(default=abid_utils.models.get_or_create_system_user_pk, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
