
from django.utils.translation import gettext_lazy as _
from django.templatetags.static import static
from django.utils.html import format_html

from wagtail import hooks

from .views import album_model_viewset, collection_chooser_viewset


@hooks.register("register_admin_viewset")
def register_viewset():
    return album_model_viewset

@hooks.register('register_admin_viewset')
def register_collection_chooser_viewset():
    return collection_chooser_viewset

