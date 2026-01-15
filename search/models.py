from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)
    segment = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    phone = models.CharField(max_length=50, null=True, blank=True)
    website = models.URLField(max_length=500, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    social_media = models.JSONField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.city}"
