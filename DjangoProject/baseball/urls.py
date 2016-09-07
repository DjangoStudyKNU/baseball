# coding: utf-8

from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from baseball import views


urlpatterns = [
    url(r'^admin/', admin.site.urls), # admin page
    url(r'^$', views.IndexView.as_view(), name="baseball"), # 프로젝트 첫 화면 
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^check/$', views.check, name='check'),
    url(r'^information/(?P<pk_id>.+)/$', views.information, name='information'),
    url(r'^university/', include('university.urls', namespace="university")),
    url(r'^amateur/', include('amateur.urls', namespace="amateur")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
