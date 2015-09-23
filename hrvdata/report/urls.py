from django.conf.urls import patterns, url
from report import views

urlpatterns = patterns('',
        url(r'^(?P<filename>.+)$', views.index),
        url(r'^$', views.index, name='report_page'),
)

