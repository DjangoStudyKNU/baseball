# coding: utf-8

from amateur.forms import SignupForm, AuthenticationForm
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib import messages




def index(request):

    var = {'comment': '사회인 야구 페이지입니다.'}

    return render(request, 'amateur/index.html', var)


