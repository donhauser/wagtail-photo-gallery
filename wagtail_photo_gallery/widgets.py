
import os

from django import forms
from django.contrib.admin.utils import quote
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe

from wagtail.coreutils import resolve_model_string


FALLBACK_TEXT = _("Click here to add an image")


class ThumbnailWidget(forms.widgets.Widget):
    """
    Widget for image thumbnails
    """
    
    @property
    def fallback_text(self):
        return FALLBACK_TEXT
    
    def render(self, name, value, attrs=None, **kwargs):
        """
        Render the thumbnail as <img> or return a <label> targeting the associated image input
        """
        
        if not value:
            # fallback to a label for the image input field, as clicking on the label will then show a file-open dialog
            html = '<label for="id_{}">{}</label>'.format(name.replace('thumb','image'), self.fallback_text)
        else:
            html = '<img src="{}"/>'.format(value.url)
        
        return mark_safe(html)
