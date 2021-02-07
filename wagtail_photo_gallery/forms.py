from django import forms

from django import forms
from wagtail.admin.forms import WagtailAdminModelForm
import PIL
import zipfile
from datetime import datetime
from django.core.files import File
from django.conf import settings


class AlbumForm(WagtailAdminModelForm):
    zip = forms.FileField(required=False, widget=forms.FileInput(attrs={'accept': '.zip'}))

    def save(self, commit=True):
        
        if self.is_valid():
            album = super().save(commit=False)
            album.modified = datetime.now()
            
            if self.cleaned_data['zip'] != None:
                
                try:
                    order = album.images.last().sort_order
                    
                except AttributeError: # no images yet
                    order = 0
                
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
