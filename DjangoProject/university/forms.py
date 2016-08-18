# coding: utf-8

from django.contrib.auth.forms import UserCreateForm, UserChangeForm
from university.models import Player

class CustomUserCreationForm(UserCreationForm):
    """
    유저 생성을 위한 폼
    """
    
    def __init__(self, *args, **kargs):
        super(CustomUserCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = Player
        fields = ("email",)

class CustomUserChangeForm(UserChangeForm):
    """
    admin 페이지에서 유저 정보 수정을 위한 폼 
    """
    
    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)
        del self.field['username']

    class Meta:
        model = Player

