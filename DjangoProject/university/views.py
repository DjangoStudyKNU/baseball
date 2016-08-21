# coding: utf-8

from django.shortcuts import render
from university.models import *
from django.views.generic import ListView, DetailView

class IndexView(DetailView):
    """
    generic view를 이용
    university 관련 플레이어의 성적 보여주기
    """
    model = Player
    template_name = "university/index.html"


