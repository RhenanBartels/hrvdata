from django.db import models
from django.contrib.auth.models import User

class SharedFile(models.Model):
    owner = models.ForeignKey(User)
    filename = models.CharField(max_length=20, default="")
    receiver = models.EmailField()
    date = models.DateTimeField(auto_now=True)
    isuser = models.BooleanField(default=True)
