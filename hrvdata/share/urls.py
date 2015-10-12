from django.conf.urls import patterns, url
from share import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='share_page'),
        url(r'^files/delete/$', views.delete_shared, name='delete_share_files_page'),
        url(r'^files/$', views.files, name='share_files_page'),
        url(r'^delete/$', views.delete, name='delete_share_page'),
)
