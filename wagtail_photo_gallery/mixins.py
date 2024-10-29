
import itertools

from django.conf import settings
from django.shortcuts import render
from django.http import Http404

from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.fields import StreamField

from .blocks import GalleryBlock
from .models import Album


WAGTAIL_IMAGE_GALLERY_DETAIL_ROUTE = getattr(settings, 'WAGTAIL_IMAGE_GALLERY_DETAIL_ROUTE', r'^album/(.+)/$')


class ImageGalleryMixin(RoutablePageMixin):
    """
    Extends the inheriting Page with a routable album detail page
    
    Every album "belonging" to a GalleryBlock on the page is served under the detail URL (default: '<page>/album/<ALBUM-SLUG>').
    Hereby, the album collection must be either the same or a descendant of the GalleryBlock's collection.
    
    Customization of the served template is possible through overriding 'album_detail_template' or 'album_detail_template_extends'.
    In the settings, WAGTAIL_IMAGE_GALLERY_DETAIL_ROUTE can be changed to set the default route.
    """
    
    album_detail_template = 'wagtail_photo_gallery/pages/album_detail.html'
    album_detail_template_extends = 'base.html'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Get a list of all StreamFields defined in this class
        # The getattr() is required to get concrete iterable instances
        self._stream_fields = [getattr(self, f.name) for f in self._meta.get_fields() if isinstance(f, StreamField)]
        
        # Filter out GalleryBlocks from each StreamField 
        self._gallery_blocks = [filter(lambda x: isinstance(x.block, GalleryBlock), f) for f in self._stream_fields]
        # Flatten the result into a single list of GalleryBlocks
        self._gallery_blocks = list(itertools.chain(*self._gallery_blocks))
        
    
    @route(WAGTAIL_IMAGE_GALLERY_DETAIL_ROUTE)
    def serve_album(self, request, slug):
        """
        Serves a referenced album in as detail page
    
        Each GalleryBlock within a StreamField is searched for the album slug.
        Invisible and non-descendant albums are excluded.
        """
        
        for gallery in self._gallery_blocks:
            try:
                collection = gallery.value['collection']
                
                album = Album.filter_by_collection(collection, is_visible=True).get(slug=slug)
                
            except Album.DoesNotExist:
                continue
            
            context = {'page': self, 'album': album}
            
            return render(
                request,
                self.album_detail_template,
                context
            )

        raise Http404
    
