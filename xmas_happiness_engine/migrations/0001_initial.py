# Generated by Django 2.0 on 2017-12-31 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.CharField(max_length=36)),
                ('text', models.CharField(max_length=100000)),
                ('title', models.CharField(max_length=255)),
            ],
        ),
    ]
