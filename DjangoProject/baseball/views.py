# coding: utf-8

from amateur.forms import SignupForm, AuthenticationForm, InformationForm, PasswordForm
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from university.models import Player
from django.contrib.auth.decorators import login_required

def index(request):
    var = {'comment': '메인페이지 입니다'}

    return render(request, 'index.html', var)



def signup(request):
    var = {} # 변수를 렌더링하기 위한 dictionary

    if request.method == "POST":
        form = SignupForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    else:
        form = SignupForm()
        var['form'] = form

    return render(request, 'signup.html', var)


def login(request):

    # 로그인 과정을 위한 폼입니다

    var = {} # 변수를 렌더하기 위한 dictionary
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(email=request.POST['email'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    django_login(request, user)
                    return redirect('/')

    else:
        form = AuthenticationForm()
        var['form'] = form

    return render(request, 'login.html',  var)


def logout(request):

    django_logout(request)

    return redirect('/')


@login_required # 로그인해야만 접속할 수 있는 페이지, 장고 기본 제공 데코레이터
def check(request):
    # 개인정보 입력전 비밀번호 확인을 통해 본인임을 확인하는 뷰입니다.
    var = {}
    if request.method == 'POST':
        form = PasswordForm(data=request.POST)
        if form.is_valid():
            user = authenticate(email=request.user.email, password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    return redirect('information', request.user.id)

    else:
        form = PasswordForm()
        var['form'] = form

    return render(request, 'check.html', var)


@login_required
def information(request, pk_id):
    # 선수에 대한 추가정보를 입력하는 폼을 조작하는 뷰입니다
    var = {}
    user = get_object_or_404(Player, id=pk_id)
    if request.method == 'POST':
        form = InformationForm(data=request.POST, files=request.FILES, instance=user)
        if form.is_valid():
            form.email = user.email
            form.password = user.password
            form.save()
            return redirect('/')

    else:
        form = InformationForm()
        var['form'] = form

    return render(request, 'information.html', var)