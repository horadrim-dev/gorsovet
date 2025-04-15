from django import template
import urllib.parse
from django.core.exceptions import ImproperlyConfigured
register = template.Library()


STYLE_CHOICES = ('all_in_one', 'list')
SIZE_CHOICES = ('micro', 'small', 'medium', 'large')
BORDER_CHOICES = ('none', 'circle')
@register.inclusion_tag("core/includes/share_buttons.html", takes_context=True)
def render_share_buttons(context, url, title, description=None, image_src=None, 
                          size="small", border="circle", style="all_in_one"):
    """
    Render social buttons for sharing
    """
    if not url or not title:
        msg = "Fields \"url\" and \"title\" must be filled.\n " + \
                "Current values: url=\"{}\", title=\"{}\""  \
                .format(url, title)
        raise ImproperlyConfigured(msg)
    
    if not description:
        description = ""
    if not image_src:
        description = ""

    host = context['request']._current_scheme_host
    absolute_image_src = host + image_src if image_src else ''
    absolute_url = host + url

    socials = []

    socials.append(('copy-button', 'link', 'Скопировать ссылку', absolute_url))

    if context['site_settings'].share_vk:
        social_url  = 'https://vk.com/share.php?';
        params = {
            'url' : absolute_url,
            'title': title,
            'description': description,
            'image' : absolute_image_src,
            'noparse':  'true'
        }
        endcoded_url = social_url + urllib.parse.urlencode(params)
        socials.append(('share-button', 'vk', 'ВКонтакте', endcoded_url))

    if context['site_settings'].share_ok:
        social_url  = 'https://connect.ok.ru/offer?';
        params = {
            'url' : absolute_url,
            'title': title,
            'description': description,
            'imageUrl' : absolute_image_src,
        }
        endcoded_url = social_url + urllib.parse.urlencode(params)
        socials.append(('share-button', 'odnoklassniki', 'Одноклассники', endcoded_url))

    if context['site_settings'].share_fb:
        social_url  = 'http://www.facebook.com/sharer.php?';
        params = {
            'u' : absolute_url,
            't': title,
        }
        endcoded_url = social_url + urllib.parse.urlencode(params)
        socials.append(('share-button', 'facebook', 'Facebook', endcoded_url))

    if context['site_settings'].share_twitter:
        social_url  = 'https://twitter.com/share?';
        params = {
            'text': title,
            'url' : absolute_url,
            'counturl' : absolute_url,
        }
        endcoded_url = social_url + urllib.parse.urlencode(params)
        socials.append(('share-button', 'twitter', 'Twitter', endcoded_url))

    return {
        'size': size if size in SIZE_CHOICES else None,
        'border': border if border in BORDER_CHOICES else None,
        'style': style if style in STYLE_CHOICES else None,
        'socials': socials,
    }


@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    """
    https://www.caktusgroup.com/blog/2018/10/18/filtering-and-pagination-django/

    Return encoded URL parameters that are the same as the current
    request's parameters, only with the specified GET parameters added or changed.

    It also removes any empty parameters to keep things neat,
    so you can remove a parm by setting it to ``""``.

    For example, if you're on the page ``/things/?with_frosting=true&page=5``,
    then

    <a href="/things/?{% param_replace page=3 %}">Page 3</a>

    would expand to

    <a href="/things/?with_frosting=true&page=3">Page 3</a>

    Based on
    https://stackoverflow.com/questions/22734695/next-and-before-links-for-a-django-paginated-query/22735278#22735278
    """
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()


@register.filter
def prepare_tag_name(tagname:str):
    """
    return same string as filter
    example: "testtag" -> "testtag", "te st tag" -> "\"te+st+tag\""
    """
    arr = tagname.split(' ')
    if len(arr) == 1:
        return tagname
    else:
        return "\"{}\"".format('+'.join(arr))
    
@register.filter
def get_type(value):
    return type(value)