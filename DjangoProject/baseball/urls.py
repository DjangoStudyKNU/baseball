# coding: utf-8

from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from baseball import views
from django.contrib.auth.views import logout_then_login

urlpatterns = [
    
    # admin page
    url(r'^admin/', admin.site.urls), 
    
    # 프로젝트 첫 화면 
    url(r'^$', views.IndexView.as_view(), name="baseball"), 
    
    ########### 확인 후 삭제  예정
    # url(r'^home/$', views.LoginCheckView.as_view(), name="home"),

    # 로그인 관련 
    url(r'^accounts/login/$', views.LoginView.as_view(), name='login'),
    url(r'^accounts/logout/$', lambda request: logout_then_login(request, "/"), name='logout'),
    
    # 회원가입 및 수정
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^check/$', views.check, name='check'),
    
    # 유저 추가 입력
    url(r'^information/(?P<pk_id>.+)/$', views.information, name='information'),
    
    # university app
    url(r'^university/', include('university.urls', namespace="university")),
    
    # amateur app
    url(r'^amateur/', include('amateur.urls', namespace="amateur")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
