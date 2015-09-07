from django.conf.urls import patterns, url
from upload import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='upload_page'),
)
