from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from FirstProjectRefactor import views as views

app_name = 'FirstProjectRefactor'
urlpatterns = [

    url(r'^admin$', admin.site.urls, name='admin'),
    url(r'^new_post/', views.new_post, name='new_post'),
    url(r'^(?P<post_id>[0-9]+)/del_post/$', views.del_post, name='del_post'),
    url(r'^(?P<post_id>[0-9]+)/change_post/$', views.change_post, name='change_post'),
    url(r'^login$', views.login_page.as_view(), name='login'),
    url(r'^loginpost/$', views.login_post, name='login_post'),
    url(r'^registration$', views.registration.as_view(), name='registration'),
    url(r'^registration/post$', views.register, name='registration_post'),

    url(r'^list/$', views.list, name='list'),
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),

    url(r'^', views.index.as_view(), name='index'),
]
