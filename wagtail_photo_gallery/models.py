
import uuid
import io
import copy
import datetime

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

from django import forms
from django.db import models
from django.core.files.base import ContentFile
from django.db.models.signals import pre_save
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from wagtail.admin.panels import FieldPanel, FieldRowPanel, ObjectList, TabbedInterface
from wagtail.models import Orderable, get_root_collection_id
from wagtail.coreutils import resolve_model_string

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from PIL import Image

from .panels import AlbumImagePanel
from .forms import AlbumForm
from .widgets import PictureWidget
from .utils import image_transpose_exif


HELP_TEXT_DETAILS = _("Indicate where and when the photos were taken. If availible, the date is used for sorting")

HELP_TEXT_IMAGES = _("""Grab an image and drag it around to change its position.
Holding down the left mouse button can be used for selecting multiple images at once, which can be dragged around with the middle mouse button.""")

ALBUM_FIELD_HELP_TEXTS = {
    'title': _("Display name of the album"),
    'date': _("When were the photos taken?"),
    'place': _("Which place can be seen on the photos?"),
    'description': _("Tell a short story about this album"),
    'image': HELP_TEXT_IMAGES,
    'zip': _("Bulk upload many images as .zip file. The images will be added to the album upon saving"),
    'slug': _("The slug of the album as it will appear in URLs e.g http://domain.com/album/[my-slug]/"),
    'collection': _("Specify to which collection the album belongs to"),
    'is_visible': _("Turn off the album's visibility to hide the album from your page"),
}

HIDDEN_PANEL_CLASS = "hidden_panel"


class Album(ClusterableModel):
    
    base_form_class = AlbumForm
    image_class = 'wagtail_photo_gallery.AlbumImage'

    collection = models.ForeignKey(
        'wagtailcore.Collection',
        default=get_root_collection_id,
        on_delete=models.CASCADE,
        related_name='+',
    )
    
    title = models.CharField(max_length=70)
    description = models.TextField(max_length=1024, blank=True)
    
    date = models.DateField(null=True, blank=True)
    place = models.CharField(null=True, blank=True, max_length=200)
    
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
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    
    
    panels = [
        FieldPanel('title', heading=_("Title"), help_text=ALBUM_FIELD_HELP_TEXTS['title']),
        FieldRowPanel([
            FieldPanel('date', heading=_("Date"), help_text=ALBUM_FIELD_HELP_TEXTS['date']),
            FieldPanel('place', heading=_("Place"), help_text=ALBUM_FIELD_HELP_TEXTS['place']),
        ], heading=_('Details'), help_text=HELP_TEXT_DETAILS),
        FieldPanel('description', heading=_("Description"), help_text=ALBUM_FIELD_HELP_TEXTS['description']),
    ]
    
    image_panels = [
        AlbumImagePanel('images', heading=_("Images"), help_text=HELP_TEXT_IMAGES),
        FieldPanel('zip', heading=_("Upload a .zip file"), help_text=ALBUM_FIELD_HELP_TEXTS['zip']),
    ]
    
    settings_panel = [
        FieldPanel('slug', help_text=ALBUM_FIELD_HELP_TEXTS['slug']),
        FieldPanel('collection', help_text=ALBUM_FIELD_HELP_TEXTS['collection']),
        FieldPanel('is_visible', help_text=ALBUM_FIELD_HELP_TEXTS['is_visible']),
    ]
    
    edit_handler = TabbedInterface([
        ObjectList(panels, heading=_('Content')),
        ObjectList(image_panels, heading=_('Images')),
        ObjectList(settings_panel, heading=_("Settings")),
    ])
    
    
    @property
    def image_model(self):
        return resolve_model_string(self.image_class)
    
    @property
    def album_cover(self):
        try:
            return mark_safe(f'<img src="{self.cover.thumb.url}" style="height: 2em; width: 2em;">')
        except:
            pass
        
        return ""
    
    @property
    def album_images(self):
        return self.images.all().count()
    
    def __str__(self):
        return self.title
    
    @classmethod
    def filter_by_collection(cls, collection, **kwargs):
        
        # get descendants INCLUDING the node itself
        query_set = collection.get_descendants(True)
        
        return Album.objects.filter(collection__in=query_set, **kwargs)
    
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
        
    def preprocess_for_db(instance=None, **kwargs):
        
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
