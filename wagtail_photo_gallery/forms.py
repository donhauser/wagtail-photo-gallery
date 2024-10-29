
import PIL
import zipfile

from datetime import datetime

from django import forms
from django.conf import settings
from django.core.files import File
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from wagtail.admin.forms import WagtailAdminModelForm


class AlbumForm(WagtailAdminModelForm):
    """
    Customized ModelForm for creating/editing an Album
    
    During saving, the Album's modified datetime is updated and the slug is set if empty/blank.
    A .zip-file upload is added to the ModelForm.
    Once uploaded, each image file in the archive is added to the album.
    """
    
    zip = forms.FileField(required=False, widget=forms.FileInput(attrs={'accept': '.zip'}))

    def save(self, commit=True):
        """
        Django model-cluster compatible save with .zip file handling for Albums
        """
        
        if self.is_valid():
            
            # pre-save with modelcluster
            album = super().save(commit=False)
            album.modified = datetime.now()
            
            if not self.cleaned_data['slug']:
                album.slug = slugify(self.cleaned_data['title'])
            
            # check if a .zip file was uploaded
            if self.cleaned_data['zip'] != None:
                
                # get the sort order position of the last image (new images should be added last)
                try:
                    order = album.images.last().sort_order
                except AttributeError: # no images yet
                    order = 0
                    
                # append every image from .zip archive 
                with zipfile.ZipFile(self.cleaned_data['zip']) as archive:

                    for index, entry in enumerate(sorted(archive.namelist())):

                        with archive.open(entry) as file:
                            
                            try:
                                img = album.image_model(name = entry, sort_order = index + order)
                                
                                img.image = File(file)
                                img.preprocess_for_db()
                                
                                album.images.add(img)
                            
                            # exclude invalid image files
                            except PIL.UnidentifiedImageError:
                                pass
            
            if commit:
                album.save()
            return album
        
        raise ValidationError(f"AlbumForm is invalid")
        
