
import os

from django import forms
from django.contrib.admin.utils import quote
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe

from wagtail.coreutils import resolve_model_string

from generic_chooser.widgets import AdminChooser


FALLBACK_TEXT = _("Click here to add an image")


class CollectionChooser(AdminChooser):
    choose_one_text = _('Choose a collection')
    choose_another_text = _('Choose another collection')
    link_to_chosen_text = _('Edit this collection')
    choose_modal_url_name = 'collection_chooser:choose'

    
    @property
    def model(self):
        return resolve_model_string('wagtailcore.Collection')

    #def get_edit_item_url(self, item):
    #    return reverse('wagtailsnippets:edit', args=('base', 'collection', quote(item.pk)))



class PictureWidget(forms.widgets.Widget):
    
    @property
    def fallback_text(self):
        return FALLBACK_TEXT
    
    def render(self, name, value, attrs=None, **kwargs):
        
        if not value:
            # fallback to a label for the image input field, as clicking on the label will then show a file-open dialog
            html = '<label for="id_{}">{}</label>'.format(name.replace('thumb','image'), self.fallback_text)
        else:
            html = '<img src="{}"/>'.format(value.url)
        
        return mark_safe(html)
