from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^quotes$', views.success),
    url(r'^logout$', views.logout),
    url(r'^addquote$', views.addquote),
    url(r'^deletequote/(?P<id>\d+)$', views.deletequote),
    url(r'^myaccount/(?P<id>\d+)$', views.show),
    url(r'^edit/(?P<id>\d+)$', views.edit),
    url(r'^like/(?P<id>\d+)$', views.like),
    url(r'^user/(?P<id>\d+)$', views.quotes),
]