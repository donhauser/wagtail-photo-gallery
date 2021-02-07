
from wagtail.core import hooks
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from wagtailcache.cache import clear_cache

from .models import Album, AlbumImage

from wagtail.admin.edit_handlers import FieldPanel


from django.utils.translation import gettext as _

class AlbumModelWagtailAdmin(ModelAdmin):
    model = Album
    menu_label = _('Albums')
    menu_icon = 'image'
    menu_order = 800
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('title', 'description')
    list_filter = ('collection',)
    #search_fields = ('fields',)

    
# Now you just need to register your customised ModelAdmin class with Wagtail
modeladmin_register(AlbumModelWagtailAdmin)

from django.templatetags.static import static
from django.utils.html import format_html

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

from .views import CollectionChooserViewSet

@hooks.register('register_admin_viewset')
def register_collection_chooser_viewset():
    return CollectionChooserViewSet('collection_chooser', url_prefix='collection-chooser')
