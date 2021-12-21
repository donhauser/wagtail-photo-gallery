# wagtail-image-gallery

With this extention you are just a few steps away from a simple photo gallery for your wagtail page.

The gallery is configurable with the wagtail admin panel and is suited for large amounts of photos.

The key idea of this project is to store and manage photos independently of the usual wagtail images.
Instead all photos are assigned to albums and can be managed by a drag-and-drop sorting widget which also supports item selection for mass-dragging and deletion.

A collection may be assigned to each album, which is then used to include all albums belonging to a collection in a `GalleryBlock`.
The `GalleryBlock` can be used in wagtails `StreamField` to embed albums into your page.

## Installation

```sh
pip install wagtail-photo-gallery
```

If you don't have pillow installed, install it via

```sh
pip install pillow
```

For the fastest possible image uploading (Faster resizing) use `pillow-simd` instead.

## Settings

```py
INSTALLED_APPS = [
    'wagtail_photo_gallery',
    'wagtail.contrib.modeladmin',
    'wagtail.contrib.routable_page',
    'generic_chooser',
]
```

Update your database structure using (remember to create a **backup first**):

```sh
./manage.py migrate
```

## Example

Once you've installed this addon and configured the settings as above,
all you need to do is to inherit from `ImageGalleryMixin` and to add `GalleryBlock` to your `StreamField`.

```py

from wagtail.core.models import Page
from wagtail.core.fields import StreamField

from wagtail.admin.edit_handlers import StreamFieldPanel

from wagtail_photo_gallery.models import GalleryBlock, ImageGalleryMixin

class YourWagtailPage(ImageGalleryMixin, Page):
    
    content = StreamField([
        #...
        ("gallery", GalleryBlock()),
        #...
    ], blank=True)
    
    # content panel for the CMS (same as always)
    content_panels = Page.content_panels + [
        StreamFieldPanel("content"),
    ]
```

If you want to use the predefined *CSS-flexbox* layout for the albums,
you need to include the following css code in your gallery page (`YourWagtailPage`)

```
{% include 'wagtail_photo_gallery/extra_css.html' %}
```


## Credits

This project was initially planned as a port of [django-photo-gallery](https://github.com/VelinGeorgiev/django-photo-gallery) as the name of this addon suggests.
Never the less, almost the entrie code is changed completely now due to incompability with wagtail and the incorporation of [django-modelcluster](https://github.com/wagtail/django-modelcluster).

Contributions to this project are welcome!

