# Generated by Django 4.2 on 2025-02-23 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Title of the about section.', max_length=255)),
                ('content', models.TextField(help_text='Detailed information about the company or website.')),
            ],
        ),
    ]
