
from django import forms
from django.utils.functional import cached_property

from wagtail.admin.panels import InlinePanel, MultiFieldPanel


class AlbumImagePanel(InlinePanel):
    
    def get_form_options(self):
        
        options = super().get_form_options()
        
        if not 'fields' in options:
            options['fields'] = []
        
        options['fields'].append('cover')
            
        if not 'widgets' in options:
            options['widgets'] = {}
        
        options['widgets']['cover'] = forms.HiddenInput()
        
        return options
    
    @cached_property
    def child_edit_handler(self):
        # hook in AlbumMultiFieldPanel instead of MultiFieldPanel
        panels = self.panel_definitions
        child_edit_handler = AlbumMultiFieldPanel(panels, heading=self.heading)
        return child_edit_handler.bind_to_model(self.db_field.related_model)
    
    
    class BoundPanel(InlinePanel.BoundPanel):
        template_name = "wagtail_photo_gallery/panels/album_image_panel.html"
        
        classes = ["album-image-panel"]
        
        class Media:
            js = ["wagtail_photo_gallery/js/album-image-panel.js"]
            css = {
                'all':[
                    "wagtail_photo_gallery/css/select-and-sort.css",
                    "wagtail_photo_gallery/css/album-image-panel.css"
                ]
            }


class AlbumMultiFieldPanel(MultiFieldPanel):
    
    class BoundPanel(MultiFieldPanel.BoundPanel):
        template_name = "wagtail_photo_gallery/panels/album_multi_field_panel.html"
        
        @cached_property
        def visible_children(self):
            return [child for child in self.children if child.is_shown() and (child.field_name == 'thumb' or '__prefix__' in child.prefix)]

        @cached_property
        def visible_children_with_identifiers(self):
            return [
                (child, identifier)
                for child, identifier in zip(
                    self.children, self.panel.child_identifiers
                )
                if child.is_shown() and child.field_name == 'thumb'
            ]
