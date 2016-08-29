# coding: utf-8

from django.shortcuts import render
from university.models import *
from django.views.generic import ListView, DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

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

class LeagueDetailView(DetailView):
    model = League

class TeamDetailView(DetailView):
    model = Team

class UniversityDetailView(DetailView):
    model = University

class LeagueList(ListView):
    model = League

class TeamList(ListView):
    model = Team

class UniversityList(ListView):
    model = University




