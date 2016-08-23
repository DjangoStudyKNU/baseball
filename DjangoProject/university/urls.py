from django.conf.urls import url 
from university import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^league/(?P<pk>\d+)/$', views.LeagueDetailView.as_view(), name='league_detail'),
    url(r'^team/(?P<pk>\d+)/$', views.TeamDetailView.as_view(), name='team_detail'),
    url(r'^uni_info/(?P<pk>\d+)/$', views.UniversityDetailView.as_view(), name='university_detail'),
]
