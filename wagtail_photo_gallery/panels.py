from django.utils.functional import cached_property

from wagtail.admin.panels import InlinePanel, MultiFieldPanel


class AlbumInlinePanel(InlinePanel):
    
    @cached_property
    def child_edit_handler(self):
        panels = self.panel_definitions
        child_edit_handler = AlbumMultiFieldPanel(panels, heading=self.heading)
        return child_edit_handler.bind_to_model(self.db_field.related_model)
    
    
    class BoundPanel(InlinePanel.BoundPanel):
        template_name = "wagtail_photo_gallery/admin/inline_panel.html"
        
        classes = ["album-inline-panel"]


class AlbumMultiFieldPanel(MultiFieldPanel):
    
    class BoundPanel(MultiFieldPanel.BoundPanel):
        template_name = "wagtail_photo_gallery/admin/multi_field_panel.html"
        
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
