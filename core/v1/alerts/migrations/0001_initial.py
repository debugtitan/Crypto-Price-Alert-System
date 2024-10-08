# Generated by Django 5.0.8 on 2024-08-11 18:45

import core.utils.enums.base
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_last_updated', models.DateTimeField(auto_now=True)),
                ('target_price', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='target price')),
                ('triggered', models.BooleanField(default=False, help_text='treat alert as triggered')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alerts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(core.utils.enums.base.BaseModelBaseMixin, models.Model),
        ),
    ]
