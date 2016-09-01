# coding: utf-8

from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.conf import settings

class Region(models.Model):
   """
   table for Region
   """
   name = models.CharField(max_length=20)

   def __str__(self):
        return self.name


class AmateurTeam(models.Model):
    """Information of team
    """
    name = models.CharField(max_length=50)
    logo = models.ImageField(blank=True)
    manager = models.CharField(max_length=20, blank=True)
    region = models.ForeignKey(Region)
    rate = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)

    def __str__(self):
        return self.name


class AmateurLeague(models.Model):
    """각 리그별 기본 정보
    전체 리그 기간 계산 : start_date  - finish_date
    """
    name = models.CharField(max_length=100)
    logo = models.ImageField()
    manager = models.CharField(max_length=20, blank=True)
    start_date = models.DateField(auto_now_add=True)
    finish_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name


class AmateurGamePlace(models.Model):
    """게임이 진행되는 경기장 정보
    데이터 입력해놓고 사용자가 선택하는 방식
    """
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100, blank=True) # 경기장 주소

    def __str__(self):
        return self.name


class AmateurGameSchedule(models.Model):

    league = models.ForeignKey(AmateurLeague) # foreignkey를 기준으로 리그별 경기 구별
    game_date = models.DateField(blank=True)
    team = models.CharField(max_length=100, blank=True) # 모델상에서는 데이터를 하나만 가지고 있지만 이후에 form상에서 두개의 팀을 입력할 수 있도록 활용.
    place = models.ForeignKey(AmateurGamePlace)

    def __str__(self):
        return self.league.name + " 리그의 "+ str(self.game_date) + " 경기"


class AmateurTeamHasLeague(models.Model):
    """리그별 팀 기록
    """
    team = models.ForeignKey(AmateurTeam)
    league = models.ForeignKey(AmateurLeague)
    win = models.PositiveSmallIntegerField(blank=True, null=True)
    lose = models.PositiveSmallIntegerField(blank=True, null=True)
    draw = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return self.league.name + "에 속한 " + self.team.name + " 팀"


class AmateurPitcherHasTeam(models.Model):
    """각 투수별 팀 기록
    """
    player = models.ForeignKey("university.Player", null=True)
    team = models.ForeignKey(AmateurTeam)
    game = models.PositiveSmallIntegerField(blank=True, null=True) # 등판 경기 수
    win = models.PositiveSmallIntegerField(blank=True, null=True) # 승리
    lose = models.PositiveSmallIntegerField(blank=True, null=True) # 패배
    inings = models.PositiveSmallIntegerField(blank=True, null=True) # 이닝 수
    saves = models.PositiveSmallIntegerField(blank=True, null=True) # 세이브
    hold = models.PositiveSmallIntegerField(blank=True, null=True) # 홀드
    hit = models.PositiveSmallIntegerField(blank=True, null=True) # 피안타 갯수
    HR = models.PositiveSmallIntegerField(blank=True, null=True) # 피홈런 갯수
    run = models.PositiveSmallIntegerField(blank=True, null=True) # 실점
    BB = models.PositiveSmallIntegerField(blank=True, null=True) # 볼넷
    HBP = models.PositiveSmallIntegerField(blank=True, null=True) # 사구
    K = models.PositiveSmallIntegerField(blank=True, null=True) # 삼진
    pitches = models.PositiveIntegerField(blank=True, null=True) # 던진 공 갯수

    def __str__(self):
        return self.team.name +" 팀의 " + self.player.name


class AmateurHitterHasTeam(models.Model):
    """각 타자별 팀 기록
    """
    player = models.ForeignKey("university.Player", null=True)
    team = models.ForeignKey(AmateurTeam)
    AB = models.PositiveSmallIntegerField(blank=True, null=True) # 타수
    H = models.PositiveSmallIntegerField(blank=True, null=True) # 안타
    double = models.PositiveSmallIntegerField(blank=True, null=True) # 2루타
    triple = models.PositiveSmallIntegerField(blank=True, null=True) # 3루타
    HR = models.PositiveSmallIntegerField(blank=True, null=True) # 홈런
    R = models.PositiveSmallIntegerField(blank=True, null=True) # 득점
    RBI = models.PositiveSmallIntegerField(blank=True, null=True) # 타점
    BB = models.PositiveSmallIntegerField(blank=True, null=True) # 볼넷
    HBP = models.PositiveSmallIntegerField(blank=True, null=True) # 사구
    K = models.PositiveSmallIntegerField(blank=True, null=True) # 삼진
    SB = models.PositiveSmallIntegerField(blank=True, null=True) # 도루 성공
    CS = models.PositiveSmallIntegerField(blank=True, null=True) # 도루 실패
    game = models.PositiveSmallIntegerField(blank=True, null=True) # 출장 게임 수

    def __str__(self):
        return self.team.name +" 팀의 " + self.player.name


class AmateurPitcherHasLeague(models.Model):
    """각 투수별 리그 성적
    """
    player = models.ForeignKey("university.Player", null=True)
    league = models.ForeignKey(AmateurLeague)
    game = models.PositiveSmallIntegerField(blank=True, null=True) # 등판 경기 수
    inings = models.PositiveSmallIntegerField(blank=True, null=True) # 이닝 수
    win = models.PositiveSmallIntegerField(blank=True, null=True) # 승리
    lose = models.PositiveSmallIntegerField(blank=True, null=True) # 패배
    saves = models.PositiveSmallIntegerField(blank=True, null=True) # 세이브
    hold = models.PositiveSmallIntegerField(blank=True, null=True) # 홀드
    hit = models.PositiveSmallIntegerField(blank=True, null=True) # 피안타 갯수
    HR = models.PositiveSmallIntegerField(blank=True, null=True) # 피홈런 갯수
    run = models.PositiveSmallIntegerField(blank=True, null=True) # 실점
    BB = models.PositiveSmallIntegerField(blank=True, null=True) # 볼넷
    HBP = models.PositiveSmallIntegerField(blank=True, null=True) # 사구
    K = models.PositiveSmallIntegerField(blank=True, null=True) # 삼진
    pitches = models.PositiveSmallIntegerField(blank=True, null=True) # 던진 공 갯수

    def __str__(self):
        return self.league.name +" 리그의 " + self.player.name


class AmateurHitterHasLeague(models.Model):
    """각 타자별 리그 성적
    """
    player = models.ForeignKey("university.Player", null=True)
    league = models.ForeignKey(AmateurLeague)
    AB = models.PositiveSmallIntegerField(blank=True, null=True) # 타수
    H = models.PositiveSmallIntegerField(blank=True, null=True) # 안타
    double = models.PositiveSmallIntegerField(blank=True, null=True) # 2루타
    triple = models.PositiveSmallIntegerField(blank=True, null=True) # 3루타
    HR = models.PositiveSmallIntegerField(blank=True, null=True) # 홈런
    R = models.PositiveSmallIntegerField(blank=True, null=True) # 득점
    RBI = models.PositiveSmallIntegerField(blank=True, null=True) # 타점
    BB = models.PositiveSmallIntegerField(blank=True, null=True) # 볼넷
    HBP = models.PositiveSmallIntegerField(blank=True, null=True) # 사구
    K = models.PositiveSmallIntegerField(blank=True, null=True) # 삼진
    SB = models.PositiveSmallIntegerField(blank=True, null=True) # 도루 성공
    CS = models.PositiveSmallIntegerField(blank=True, null=True) # 도루 실패
    game = models.PositiveSmallIntegerField(blank=True, null=True) # 출장 게임 수

    def __str__(self):
        return self.league.name +" 리그의 " + self.player.name


class AmateurGameDetailHitter(models.Model):
    """각 게임 세부 정보 및
    타자 기록
    """
    player = models.ForeignKey("university.Player", null=True)
    game = models.ForeignKey(AmateurGameSchedule)
    ining_1 = models.CharField(max_length=100, blank=True) # 각 이닝 정보
    ining_2 = models.CharField(max_length=100, blank=True) # 각 이닝 정보
    ining_3 = models.CharField(max_length=100, blank=True) # 각 이닝 정보
    ining_4 = models.CharField(max_length=100, blank=True) # 각 이닝 정보
    ining_5 = models.CharField(max_length=100, blank=True) # 각 이닝 정보
    ining_6 = models.CharField(max_length=100, blank=True) # 각 이닝 정보
    ining_7 = models.CharField(max_length=100, blank=True) # 각 이닝 정보
    ining_8 = models.CharField(max_length=100, blank=True) # 각 이닝 정보
    ining_9 = models.CharField(max_length=100, blank=True) # 각 이닝 정보
    AB = models.PositiveSmallIntegerField(blank=True, null=True) # 타수
    hit = models.PositiveSmallIntegerField(blank=True, null=True) # 안타
    run = models.PositiveSmallIntegerField(blank=True, null=True) # 득점
    RBI = models.PositiveSmallIntegerField(blank=True, null=True) # 타점
    SB = models.PositiveSmallIntegerField(blank=True, null=True) # 도루 성공
    CS = models.PositiveSmallIntegerField(blank=True, null=True) # 도루 실패
    BB = models.PositiveSmallIntegerField(blank=True, null=True) # 볼넷
    HBP = models.PositiveSmallIntegerField(blank=True, null=True) # 사구

    def __str__(self):
        return str(self.game.game_date) + " 경기 " + self.player.name + "선수 성적"


class AmateurGameDetailPitcher(models.Model):
    """각 게임별 투수 세부 기록
    """
    game = models.ForeignKey(AmateurGameSchedule)
    player = models.ForeignKey("university.Player", null=True)
    win = models.NullBooleanField() # 승패
    saves = models.NullBooleanField() # 세이브 여부
    hold = models.NullBooleanField() # 홀드 여부
    HR = models.PositiveSmallIntegerField(blank=True, null=True) # 피홈런
    hit = models.PositiveSmallIntegerField(blank=True, null=True) # 피안타
    K = models.PositiveSmallIntegerField(blank=True, null=True) # 탈삼진
    run = models.PositiveSmallIntegerField(blank=True, null=True) # 실점
    BB = models.PositiveSmallIntegerField(blank=True, null=True) # 볼넷
    HBP = models.PositiveSmallIntegerField(blank=True, null=True) # 사구
    pitches = models.PositiveSmallIntegerField(blank=True, null=True) # 공갯수

    def __str__(self):
        return str(self.game.game_date) + " 경기 " + self.player.name  + "선수 성적"


