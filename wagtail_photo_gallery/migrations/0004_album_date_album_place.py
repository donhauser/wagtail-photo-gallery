# Generated by Django 4.2 on 2024-10-19 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtail_photo_gallery', '0003_alter_album_collection'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='album',
            name='place',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]