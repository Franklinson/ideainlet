# Generated by Django 4.2.10 on 2024-02-21 03:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('abstract', '0004_rename_statuses_statuse_rename_event_topics_topic'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='abstract',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='abstract.abstract'),
        ),
    ]
