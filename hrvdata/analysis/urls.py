from django.conf.urls import patterns, url
from analysis import views

urlpatterns = patterns('',
        #url(r'^(?P<filename>\d{8,10})$', views.index, name='analysis_page'),
        url(r'^(?P<filename>.+)/(?P<indexname>[a-z]+([a-z]+|[0-9]+i)_li)/$',
            views.change_tv_index, name='analysis_page'),
        url(r'^(?P<filename>.+)$', views.index, name='analysis_page'),
)
