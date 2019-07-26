from django.db import models

# Create your models here.
class RandomId(models.Model):
    random_id = models.TextField(null=False, blank=False)