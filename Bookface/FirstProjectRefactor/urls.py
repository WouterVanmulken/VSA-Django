from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static as static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from FirstProjectRefactor import views as views

app_name = 'FirstProjectRefactor'

urlpatterns = staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [

    url(r'^admin', admin.site.urls, name='admin'),
    url(r'^new_post/', views.new_post, name='new_post'),
    url(r'^(?P<post_id>[0-9]+)/del_post/$', views.del_post, name='del_post'),
    url(r'^(?P<post_id>[0-9]+)/change_post/$', views.change_post, name='change_post'),
    url(r'^login/$', views.login_page.as_view(), name='login'),
    url(r'^logout$', views.logout_view, name='logout'),
    url(r'^loginpost/$', views.login_post, name='login_post'),
    url(r'^registration$', views.Registration.as_view(), name='registration'),
    url(r'^registration/post$', views.register, name='registration_post'),

    url(r'^(?P<post_id>[0-9]+)/like$', views.like, name='like'),
    url(r'^(?P<post_id>[0-9]+)/hasliked/$', views.has_liked, name='has_liked'),


    url(r'^list$', views.list, name='list'),
    url(r'^search$', views.search, name='search'),
    url(r'^friends$', views.friends, name='friends'),
    url(r'^addfriend/(?P<user_name>[A-Za-z0-9]+)$', views.add_friend, name='add_friend'),
    url(r'^profile/(?P<user_name>[A-Za-z0-9]+)$', views.profile, name='profile'),

    url(r'^(?P<page>[A-Za-z0-9]+)$', views.index3, name='aaa'),
    url(r'^', views.index2, name='index'),
]
