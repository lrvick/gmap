import json
import urllib
import urllib2
from django.db import models


class MarkerType(models.Model):
    category_name = models.CharField("type", max_length=200, unique=True)

    def __unicode__(self):
        return self.category_name


class MapMarker(models.Model):
    name = models.CharField(max_length=200)
    latitude = models.CharField(max_length=20, blank=True)
    longitude = models.CharField(max_length=20, blank=True)
    marker_type = models.ForeignKey(MarkerType, "category_name")
    airport_code = models.CharField(max_length=6, blank=True)
    address = models.TextField(max_length=200)
    phone = models.CharField(max_length=40, blank=True)
    fax = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)
    url = models.URLField(blank=True)

    # Make sure we update the lat/long with the location
    def save(self, *args, **kwargs):
        # TODO: Move the geolocation into a function somewhere
        url = "http://maps.googleapis.com/maps/api/geocode/json?"
        url += urllib.urlencode({'address': self.address, 'sensor': 'false'})
        data = urllib2.urlopen(url).read()
        data = json.loads(data)
        self.latitude = data['results'][0]['geometry']['location']['lat']
        self.longitude = data['results'][0]['geometry']['location']['lng']
        super(MapMarker, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name