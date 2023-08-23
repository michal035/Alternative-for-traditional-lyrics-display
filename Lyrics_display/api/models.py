from django.db import models


class User(models.Model):
    username = models.CharField(max_length=200,null=True, blank=True)
    passwd = models.CharField(max_length=200,null=True, blank=True)



class Doc(models.Model):
    token = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

