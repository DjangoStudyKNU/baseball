# coding: utf-8

from django.shortcuts import redirect, render


def index(request):
    var = {'comment': '메인페이지 입니다'}

    return render(request, 'index.html', var)



