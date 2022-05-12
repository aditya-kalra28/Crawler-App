from django.db import models

# Create your models here.
class page(models.Model):
    num = models.IntegerField(default=0,blank=True)
    link = models.CharField(max_length=1000)
    creator = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    published_date = models.CharField(max_length=200)
    reading_time = models.CharField(max_length=200)