
from wagtail.core.utils import resolve_model_string

from django.contrib.admin.utils import quote
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from generic_chooser.widgets import AdminChooser

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



from django.conf import settings
from django import forms
from string import Template
from django.utils.safestring import mark_safe
import os


class PictureWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None, **kwargs):
        
        if not value:
            html = '<label style="display: block; width: 100%; height: 100%;" for="id_{}">Click here to add an image</label>'.format(name.replace('thumb','image'))
        else:
            html = '<img style="max-width: 100px; max-height: 100px;" src="{}"/>'.format(value.url)
        
        return mark_safe(html)
