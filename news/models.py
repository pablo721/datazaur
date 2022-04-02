from django.db import models



class Website(models.Model):
    title = models.CharField(max_length=64)
    url = models.CharField(max_length=128)
    selector = models.CharField(max_length=128, blank=True)



class Article(models.Model):
    url = models.CharField(max_length=128)
    source = models.CharField(max_length=64)
    headline = models.CharField(max_length=128)
    text = models.TextField(blank=True)
