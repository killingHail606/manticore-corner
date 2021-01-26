from django.db import models
from django.urls import reverse


class Hero(models.Model):
    name = models.CharField(max_length=100)
    picture_for_wall = models.ImageField(upload_to='wall_of_heroes/%Y/%m/%d')
    picture_for_detail = models.ImageField(upload_to='wall_of_heroes/%Y/%m/%d', blank=True)
    short_biography = models.TextField()
    influenced_me = models.TextField()
    quotes = models.TextField()
    date_pub = models.DateField(auto_now_add=True)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('wall_of_heroes:hero_detail', args=[self.slug])
