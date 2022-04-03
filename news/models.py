from django.db import models


class Selector(models.Model):
    text = models.CharField(max_length=128, unique=True)


class Website(models.Model):
    title = models.CharField(max_length=64, blank=True)
    url = models.CharField(max_length=128)
    selectors = models.ManyToManyField('news.Selector', related_name='website_selector', blank=True)



class Article(models.Model):
    url = models.CharField(max_length=128)
    source = models.CharField(max_length=64)
    headline = models.CharField(max_length=128)
    text = models.TextField(blank=True)
