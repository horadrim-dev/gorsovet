from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.models import CMSPlugin
from django.conf import settings

class YandexMap(CMSPlugin):
    """
    A yandex maps integration
    """
    title = models.CharField(_("название"), max_length=100)
    
    address = models.CharField(_("адрес"), max_length=150, blank=True, null=True)
    zipcode = models.CharField(_("почтовый индекс"), max_length=30, blank=True, null=True)
    city = models.CharField(_("город"), max_length=100, blank=True, null=True)
    
    zoom = models.IntegerField(_("zoom (уровень масштаба)"), blank=True, null=True)
    
    lat = models.DecimalField(_('широта'), max_digits=10, decimal_places=6, null=True, blank=True)
    lng = models.DecimalField(_('долгота'), max_digits=10, decimal_places=6, null=True, blank=True)
    
    
    def __unicode__(self):
        return u"%s (%s, %s %s)" % (self.get_title(), self.address, self.zipcode, self.city,)
    
    def full_address(self):
        return ", ".join([x for x in [self.zipcode, self.city, self.address] if x])

    def get_title(self):
        if self.title == None:
            return _("Карта")
        return self.title
    
    def get_zoom_level(self):
        if self.zoom == None:
            return 13
        return self.zoom
    
    def get_lat_lng(self):
        if self.lat and self.lng:
            return [float(self.lat), float(self.lng)]
        return ''

    def get_api_key(self):
        return settings.YANDEX_MAPS_API_KEY 