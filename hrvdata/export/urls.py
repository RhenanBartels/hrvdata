from django.conf.urls import patterns, url
from export import views

urlpatterns = patterns('',
        url(r'^(?P<filename>\d{8,10})$', views.index, name='export_page'),
)
