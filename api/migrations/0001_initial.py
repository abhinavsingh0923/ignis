# Generated by Django 5.0.6 on 2024-06-10 17:03

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coin', models.CharField(max_length=10)),
                ('output', models.JSONField()),
                ('status', models.CharField(default='pending', max_length=20)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='api.job')),
            ],
        ),
    ]
