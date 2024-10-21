
from django.utils.translation import gettext_lazy as _
from django.templatetags.static import static
from django.utils.html import format_html

from wagtail import hooks

from .views import album_model_viewset
from .views import collection_chooser_viewset


SELECT_AND_SORT_JS = "wagtail_photo_gallery/admin/js/select-and-sort.js"
SELECT_AND_SORT_CSS = "wagtail_photo_gallery/admin/css/select-and-sort.css"


@hooks.register("insert_global_admin_css", order=100)
def global_admin_css():
    
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static(SELECT_AND_SORT_CSS)
    )

@hooks.register("insert_global_admin_js", order=100)
def global_admin_js():
    
    return format_html(
        '<script src="{}"></script>',
        static(SELECT_AND_SORT_JS)
    )

@hooks.register("register_admin_viewset")
def register_viewset():
    return album_model_viewset

@hooks.register('register_admin_viewset')
def register_collection_chooser_viewset():
    return collection_chooser_viewset

