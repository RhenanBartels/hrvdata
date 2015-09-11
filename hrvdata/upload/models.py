from django.db import models
from django.contrib.auth.models import User

class Tachogram(models.Model):
    owner = models.ForeignKey(User)
    filename = models.CharField(max_length=20)
    rri = models.FileField()

    def delete(self, *args, **kwargs):
        storage, path = self.rri.storage, self.rri.path
        super(Tachogram, self).delete(*args, **kwargs)
        storage.delete(path)

User.profile = property(lambda u: Image.objects.get_or_create(owner=u)[0])
