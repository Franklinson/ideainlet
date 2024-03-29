# Generated by Django 4.2.10 on 2024-02-20 02:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Abstract_form',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, null=True)),
                ('abstract_body', models.CharField(max_length=600, null=True)),
                ('keywords', models.CharField(max_length=300, null=True)),
                ('author_name', models.CharField(max_length=200, null=True)),
                ('author_email', models.CharField(max_length=200, null=True)),
                ('author_affiliation', models.CharField(max_length=200, null=True)),
                ('presenter_name', models.CharField(max_length=200, null=True)),
                ('presenter_email', models.CharField(max_length=200, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('Mr.', 'Mr.'), ('Mrs', 'Mrs.'), ('Dr.', 'Dr.'), ('Prof.', 'Prof.')], max_length=50)),
                ('first_name', models.CharField(max_length=200, null=True)),
                ('last_name', models.CharField(max_length=200, null=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=50)),
                ('phone', models.CharField(max_length=200, null=True)),
                ('email', models.CharField(max_length=200, null=True)),
                ('profession', models.CharField(max_length=200, null=True)),
                ('organization', models.CharField(max_length=200, null=True)),
                ('address', models.CharField(max_length=300, null=True)),
                ('bio', models.CharField(blank=True, max_length=600, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event_topics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topics', models.CharField(max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Presentation_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('presentation_preference', models.CharField(max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Abstract_status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Under Review', 'Under Review'), ('Accepted', 'Accepted'), ('Rejected.', 'Rejected')], max_length=50)),
                ('abstract_form', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='abstract.abstract_form')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='abstract.author')),
            ],
        ),
        migrations.AddField(
            model_name='abstract_form',
            name='presentation_preference',
            field=models.ManyToManyField(to='abstract.presentation_type'),
        ),
        migrations.AddField(
            model_name='abstract_form',
            name='topics',
            field=models.ManyToManyField(to='abstract.event_topics'),
        ),
    ]
