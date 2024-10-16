# Generated by Django 4.0 on 2024-10-12 10:50

from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail_photo_gallery.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_homepage_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='content',
            field=wagtail.fields.StreamField([('gallery', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock()), ('collection', wagtail_photo_gallery.blocks.CollectionChooserBlock())]))], blank=True, use_json_field=True),
        ),
    ]
