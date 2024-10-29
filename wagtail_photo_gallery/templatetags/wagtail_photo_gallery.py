from django import template
from ..models import Album


register = template.Library()


@register.inclusion_tag('wagtail_photo_gallery/tags/include_album.html', takes_context=True)
def include_album(context, album, page=None):
    """
    Include a preview of the given album
    """
    
    request = context['request']
    
    if page is None:
        page = context['page']
        
    if request.is_preview: # fix for invalid detail URL in preview mode
        detail_url = ""
    else:
        detail_url = page.url + page.reverse_subpage('serve_album', args=[album.slug])

    return {
        'album': album,
        'detail_url': detail_url,
    }


@register.inclusion_tag('wagtail_photo_gallery/tags/include_album_detail.html', takes_context=False)
def include_album_detail(album):
    """
    Include the given album with details and images
    """
    
    return {
        'album': album,
        'images': album.images.all(),
    }


@register.simple_tag(takes_context=False)
def get_albums(collection=None, ascending=False):
    """
    Query visible albums for the given collection
    
    An album belongs to the collection if the album collection is equal or a descendant of the given collection.
    If no collection is given, every visible album is returned
    """
    
    if collection is None:
        albums = Album.objects.filter(is_visible=True)
    else:
        albums = Album.filter_by_collection(collection, is_visible=True)
    
    if ascending:
        order = ['date', 'created']
    else:
        order = ['-date', '-created']
        
    return albums.order_by(*order)
