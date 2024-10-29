
from django import forms
from django.utils.functional import cached_property

from wagtail.admin.panels import InlinePanel, MultiFieldPanel


class AlbumImagePanel(InlinePanel):
    """
    Panel for managing larger amounts of album images
    
    Images are rendered as interactive thumbnails to support easy selection, sorting and deletion.
    Under the hood the InlinePanel form functionality is used.
    """
    
    def get_form_options(self):
        """
        Adapted form options for album image management
    
        The album's 'cover' image is added as HiddenInput to make it accessible within this panel
        """
        
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
        """
        Initialize an AlbumMultiFieldPanel for managing the related object/image fields
        """
        
        panels = self.panel_definitions
        child_edit_handler = AlbumMultiFieldPanel(panels, heading=self.heading)
        return child_edit_handler.bind_to_model(self.db_field.related_model)
    
    
    class BoundPanel(InlinePanel.BoundPanel):
        """
        Album panel that is bounded to a concrete Album instance
        """
        
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
    """
    Panel for managing the related object/image fields of an Album
    """
    
    class BoundPanel(MultiFieldPanel.BoundPanel):
        """
        Panel that is bounded to a concrete AlbumImage instance
        """
        
        template_name = "wagtail_photo_gallery/panels/album_multi_field_panel.html"
        
        @cached_property
        def visible_children(self):
            """
            Visible fields in the form
        
            In general, only the 'thumb' field is visible, but for new images every input field is added.
            """
            return [child for child in self.children if child.is_shown() and (child.field_name == 'thumb' or '__prefix__' in child.prefix)]

        @cached_property
        def visible_children_with_identifiers(self):
            """
            Visible fields with identifiers in the form
        
            Only the 'thumb' field is visible
            """
            return [
                (child, identifier)
                for child, identifier in zip(
                    self.children, self.panel.child_identifiers
                )
                if child.is_shown() and child.field_name == 'thumb'
            ]
