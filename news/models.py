from django.db import models


class Website(models.Model):
    title = models.CharField(max_length=64, blank=True)
    url = models.CharField(max_length=128, blank=False)
    selectors = models.CharField(max_length=256, blank=True)

