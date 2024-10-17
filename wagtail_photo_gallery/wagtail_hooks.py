
from django.utils.translation import gettext_lazy as _
from django.templatetags.static import static
from django.utils.html import format_html

from wagtail import hooks

from .views import album_model_viewset
from .views import collection_chooser_viewset


@hooks.register("insert_global_admin_css", order=100)
def global_admin_css():
    
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static("photo_gallery_admin.css")
    )

@hooks.register("insert_global_admin_js", order=100)
def global_admin_js():
    
    return format_html(
        '<script src="{}"></script>',
        static("photo_gallery_admin.js")
    )

@hooks.register("register_admin_viewset")
def register_viewset():
    return album_model_viewset

@hooks.register('register_admin_viewset')
def register_collection_chooser_viewset():
    return collection_chooser_viewset

