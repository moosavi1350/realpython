# Generated by Django 4.1.5 on 2023-02-03 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('name', models.CharField(blank=True, max_length=25)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
