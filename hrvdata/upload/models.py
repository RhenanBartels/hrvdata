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

class Settings(models.Model):
    signal = models.OneToOneField(Tachogram, primary_key=True)
    start_signal = models.FloatField(default=0.0)
    end_signal = models.FloatField()
    tv_segment_size = models.IntegerField(default=30)
    tv_overlap_size = models.IntegerField(default=0)
    sp_sampling_freq = models.IntegerField(default=4)
    sp_window_func = models.IntegerField(default=0)
    sp_detrending = models.IntegerField(default=0)
    sp_segment_size = models.IntegerField(default=256)
    sp_overlap_size = models.IntegerField(default=128)
    sp_model_order = models.IntegerField(default=16)
    tf_sampling_freq = models.IntegerField(default=5)
    tf_window_func = models.IntegerField(default=0)
    tf_detrending = models.IntegerField(default=0)
    tf_segment_size = models.IntegerField(default=512)
    tf_overlap_size = models.IntegerField(default=256)
    tf_model_order = models.IntegerField(default=16)

User.profile = property(lambda u: Image.objects.get_or_create(owner=u)[0])
