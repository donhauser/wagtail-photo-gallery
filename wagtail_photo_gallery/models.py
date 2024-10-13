
import uuid
import io
import copy
import itertools

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

from django import forms
from django.db import models
from django.core.files.base import ContentFile
from django.db.models.signals import pre_save, post_save
from django.shortcuts import render
from django.http import Http404
from django.utils.translation import gettext_lazy as _

from wagtail.admin.panels import HelpPanel, FieldPanel, ObjectList, TabbedInterface, MultiFieldPanel
from wagtail.models import Orderable
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.coreutils import resolve_model_string
from wagtail.fields import StreamField

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from PIL import Image

from .panels import AlbumInlinePanel
from .forms import AlbumForm
from .widgets import PictureWidget
from .utils import image_transpose_exif
from .blocks import GalleryBlock


HELP_TEXT = _("""Grab an image and drag it around to change its position.
Holding down the left mouse button can be used for selecting multiple images at once, which can be dragged around with the middle mouse button.""")

HIDDEN_PANEL_CLASS = "hidden_panel"

class Album(ClusterableModel):
    
    base_form_class = AlbumForm
    image_class = 'wagtail_photo_gallery.AlbumImage'

    collection = models.ForeignKey(
        'wagtailcore.Collection',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    
    title = models.CharField(max_length=70)
    description = models.TextField(max_length=1024)
    
    cover = models.OneToOneField(
        'wagtail_photo_gallery.AlbumImage',
        on_delete=models.SET_NULL,
        null=True,
        related_name='cover_for',
        blank=True
    )
    
    is_visible = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=50, unique=True)
    
    
    @property
    def image_model(self):
        return resolve_model_string(self.image_class)
    
    panels = [
        FieldPanel('title', heading=_("Title")),
        FieldPanel('description', heading=_("Description")),
        AlbumInlinePanel('images', heading=_("Images"), help_text=HELP_TEXT),
        FieldPanel('zip', heading=_("Upload a .zip file")),
        FieldPanel('cover', widget=forms.widgets.Input, classname=HIDDEN_PANEL_CLASS)
    ]
    
    settings_panel = [
        FieldPanel('slug'),
        FieldPanel('collection'),
        FieldPanel('is_visible'),
    ]
    
    edit_handler = TabbedInterface([
        ObjectList(panels, heading=_('Content')),
        ObjectList(settings_panel, heading=_("Settings")),
    ])
    
    def __str__(self):
        return self.title
    
    class Meta:
         verbose_name = _('Album')
         verbose_name_plural = _('Albums')


class AlbumImage(Orderable):

    name = models.CharField(max_length=255, default=None, null=True)
    
    image = ProcessedImageField(upload_to='albums', processors=[ResizeToFit(1920, 1920)], format='JPEG', options={'quality': 80})
    thumb = ProcessedImageField(upload_to='albums', processors=[ResizeToFit(300, 300)], format='JPEG', options={'quality': 80}, blank=True)
    album = ParentalKey('Album', on_delete=models.CASCADE, related_name='images')
    created = models.DateTimeField(auto_now_add=True)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    slug = models.SlugField(max_length=70, default=uuid.uuid4, editable=False)
    
    panels = [
        FieldPanel('thumb', widget=PictureWidget),
        FieldPanel('image'),
    ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._original_image = copy.copy(self.image)
        
    def preprocess_for_db(instance=None, **kwargs): # TODO self?
        
        # Skip unchanged images
        if instance._original_image == instance.image:
            return
        
        if not instance.name:
            instance.name = instance.image.name

        with instance.image.open() as f:
            
            with Image.open(f) as image:
                
                # Cameras store rotation in the exif data and django can't handle that
                image = image_transpose_exif(image)
                    
                # This needs to be after the exif fix
                processor = ResizeToFit(1920, 1920)
                image = processor.process(image)
                
                # JPEG does not support alpha
                image = image.convert("RGB")
                
                # Image to byte stream
                imgByteArr = io.BytesIO()
                image.save(imgByteArr, format='JPEG', quality=80)
                
                # Dummy file for image fields
                contentfile = ContentFile(imgByteArr.getvalue())
                
                instance.width, instance.height = image.size
                
                # random file name
                filename = uuid.uuid4().hex
                
                instance.image.save(filename, contentfile, save=False)
                instance.thumb.save('thumb-{0}'.format(filename), contentfile, save=False)

       
    @property
    def alt(self):
        return _("Album Image")
    
    def __str__(self):
        return self.name or str(super())


pre_save.connect(AlbumImage.preprocess_for_db, sender=AlbumImage)


class ImageGalleryMixin(RoutablePageMixin):
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
            
            return render(
                request,
                'wagtail_photo_gallery/album_detail.html',
                { 'page':self, 'album': album , 'images': album.images.all()}
            )

        raise Http404
    
