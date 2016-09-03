# coding: utf-8

from amateur.forms import SignupForm, AuthenticationForm
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as django_login, logout as django_logout

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