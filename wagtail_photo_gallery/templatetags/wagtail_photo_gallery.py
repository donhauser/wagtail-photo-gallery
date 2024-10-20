from django import template
from ..models import Album


register = template.Library()


@register.inclusion_tag('wagtail_photo_gallery/tags/include_album.html', takes_context=True)
def include_album(context, album, page=None):
    request = context['request']
    
    if page is None:
        page = context['page']
        
    if request.is_preview: # fix for invalid detail url in preview mode
        detail_url = ""
    else:
        detail_url = page.url + page.reverse_subpage('serve_album', args=[album.slug])

    return {
        'album': album,
        'detail_url': detail_url,
    }


@register.inclusion_tag('wagtail_photo_gallery/tags/include_album_detail.html', takes_context=True)
def include_album_detail(context, album):
    
    return {
        'album': album,
        'images': album.images.all(),
    }
