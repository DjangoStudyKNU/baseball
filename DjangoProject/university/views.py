# coding: utf-8

from django.shortcuts import render
from university.models import *
from django.views.generic import ListView, DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

################ university index view ####################
class IndexView(ListView):
    """
    generic view를 이용
    university 관련 플레이어의 성적 보여주기
    """
    template_name = "university/index.html"
    context_object_name = "player_data"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return Player.objects.filter(id=self.request.user.id)[0]

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['object_list'] = ['Team', 'League', 'University']
        return context


############################ 디테일 뷰 ####################### 

class PlayerDetailView(DetailView):
    """각 플레이어의 세부 뷰 
    """
    # url, templates 
    model = Player 

class LeagueDetailView(DetailView):
    """각 리그의 세부 뷰
    """
    model = UniversityLeague

class TeamDetailView(DetailView):
    """각 팀의 세부 뷰
    """
    model = UniversityTeam

class UniversityDetailView(DetailView):
    """각 학교의 세부 뷰
    """
    model = University

class GamePlaceDetailView(DetailView):
    """각 경기장 세부 뷰
    """
    # url, templates 
    model = UniversityGamePlace

class GameScheduleDetailView(DetailView):
    """각 경기 일정 세부 정부 
    """
    # url, templates 
    model = UniversityGameSchedule




############### 리스트 뷰 #################### 

class PlayerList(ListView):
    """Player 리스트 뷰 
    """
    # url, templates 
    model = Player

class LeagueList(ListView):
    """Legue들의 리스트 뷰
    """
    model = UniversityLeague

class TeamList(ListView):
    """Team들의 리스트 뷰
    """
    model = UniversityTeam

class UniversityList(ListView):
    """각 University들의 리스트
    """
    model = University

class GamePlaceList(ListView):
    """각 경기장 리스트 
    """
    # url, templates 
    model = UniversityGamePlace


class GameScheduleList(ListView):
    """각 경기 일정 리스트 
    """
    # url, templates 
    model = UniversityGameSchedule


