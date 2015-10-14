from django.db import models
from django.contrib.auth.models import User

from upload.models import Tachogram

class Comment(models.Model):
    author = models.ForeignKey(User)
    signal = models.ForeignKey(Tachogram)
    text = models.TextField()
    created_time = models.DateTimeField(auto_now=True)
    edited = models.BooleanField(default=False)


User.profile = property(lambda u: Image.objects.get_or_create(owner=u)[0])
