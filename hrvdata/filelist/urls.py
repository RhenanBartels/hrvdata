from django.conf.urls import patterns, url
from filelist import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='filelist_page'),
        url(r'^delete/$', views.delete, name='delete_page'),
)
