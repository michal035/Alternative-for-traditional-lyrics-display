from django.db import models


class doc(models.Model):
    passwd = models.CharField(max_length=200,null=True, blank=True)
    token = models.CharField(max_length=20)

