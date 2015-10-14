from django.conf.urls import patterns, url
from analysis import views

urlpatterns = patterns('',
        #url(r'^(?P<filename>\d{8,10})$', views.index, name='analysis_page'),
        url(r'^shared/(?P<filename>.+)/(?P<indexname>[a-z]+([a-z]+|[0-9]+i)_li)/$',
            views.change_tv_index_shared),
        url(r'^(?P<filename>.+)/(?P<indexname>[a-z]+([a-z]+|[0-9]+i)_li)/$',
            views.change_tv_index),
        url(r'^shared/(?P<filename>.+)/comment$', views.comment),
        url(r'^shared/(?P<filename>.+)$', views.shared, name='analysis_shared_page'),
        url(r'^(?P<filename>.+)/settings$', views.settings),
        url(r'^(?P<filename>.+)$', views.index, name='analysis_page'),
)
