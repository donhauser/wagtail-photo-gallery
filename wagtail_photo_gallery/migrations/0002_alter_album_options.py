# Generated by Django 4.0 on 2024-10-13 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtail_photo_gallery', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='album',
            options={'verbose_name': 'Album', 'verbose_name_plural': 'Albums'},
        ),
    ]