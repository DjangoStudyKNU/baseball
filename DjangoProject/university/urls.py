from django.conf.urls import url 
from university import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    
    # detail 
    url(r'^league/(?P<pk>\d+)/$', views.LeagueDetailView.as_view(), name='league_detail'),
    url(r'^team/(?P<pk>\d+)/$', views.TeamDetailView.as_view(), name='team_detail'),
    url(r'^university/(?P<pk>\d+)/$', views.UniversityDetailView.as_view(), name='university_detail'),

    # list
    url(r'^league/$', views.LeagueList.as_view(), name='league_list'),
    url(r'^team/$', views.TeamList.as_view(), name='team_list'),
    url(r'^university/$', views.UniversityList.as_view(), name='university_list'),
]
