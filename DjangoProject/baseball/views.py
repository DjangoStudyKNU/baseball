# coding: utf-8

from amateur.forms import SignupForm, InformationForm, PasswordForm#, AuthenticationForm
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from university.models import Player
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import AuthenticationForm
from django.utils.http import is_safe_url
from django.contrib.auth import REDIRECT_FIELD_NAME 
from django.views.generic import TemplateView, ListView, FormView, RedirectView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters



class IndexView(TemplateView):
    """프로젝트 루트 페이지 
    """
    template_name = 'index.html'
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

class LoginView(FormView):
    """
    로그인 기능
    """
    success_url = '/'
    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'login.html'

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        request.session.set_test_cookie()
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        django_login(self.request, form.get_user())
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.GET.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = self.success_url
        return redirect_to


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
