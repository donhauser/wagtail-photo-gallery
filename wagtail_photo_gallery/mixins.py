
import itertools

from django.shortcuts import render
from django.http import Http404

from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.fields import StreamField

from .blocks import GalleryBlock


class ImageGalleryMixin(RoutablePageMixin):
    album_detail_template = 'wagtail_photo_gallery/pages/album_detail.html'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Get a list of all StreamFields defined in this class
        # The getattr() is required to get concrete iterable instances
        self._stream_fields = [getattr(self, f.name) for f in self._meta.get_fields() if isinstance(f, StreamField)]
        
        # Filter out GalleryBlocks from each StreamField 
        self._gallery_blocks = [filter(lambda x: isinstance(x.block, GalleryBlock), f) for f in self._stream_fields]
        # Flatten the result into a single list of GalleryBlocks
        self._gallery_blocks = list(itertools.chain(*self._gallery_blocks))
        
    
    @route(r'^album/(.+)/$')
    def serve_album(self, request, slug):
        
        # search for the album slug in all gallery blogs
        for gallery in self._gallery_blocks:
            try:
                album = gallery.block.filter_albums(gallery.value).get(slug=slug)
                
            except Album.DoesNotExist:
                continue
            
            context = {'page': self, 'album': album, 'images': album.images.all()} # images is required for extra_js
            
            return render(
                request,
                self.album_detail_template,
                context
            )

        raise Http404
    
