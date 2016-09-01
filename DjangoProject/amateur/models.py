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


class Team(models.Model):
    """Information of team
    """
    name = models.CharField(max_length=50)
    logo = models.ImageField()
    manager = models.CharField(max_length=20, blank=True)
    region = models.ForeignKey(Region)
    rate = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)

    def __str__(self):
        return self.name


class League(models.Model):
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


class GamePlace(models.Model):
    """게임이 진행되는 경기장 정보
    데이터 입력해놓고 사용자가 선택하는 방식
    """
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100, blank=True) # 경기장 주소

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    """
    Player 테이블을 AbstractBaseUser 클래스로 확장하였기때문에 재정의 필요
    """

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """
        이메일과 패스워드 값을 받아서 유저 생성, 저장
        """
        now = timezone.now()
        if not email:
            raise ValueError(u'잘못된 이메일 참조')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)


class BaseUser(AbstractBaseUser, PermissionsMixin):
    """두 app의 상위 클래스
    아마추어 플레이어와 유니벓시티 플레이어의 상위 클래스
    """
    email = models.EmailField(_('email address'), unique=True, max_length=255)
    photo = models.ImageField()
    name = models.CharField(_('name'), max_length=30, blank=True)
    age = models.PositiveSmallIntegerField(blank=True, null=True) # 나이
    main_position = models.CharField(max_length=20, blank=True) # 주 포지션
    height = models.PositiveSmallIntegerField(blank=True, null=True) # 선수 키
    weight = models.PositiveSmallIntegerField(blank=True, null=True) # 선수 몸무게
    date_joined = models.DateTimeField(default=timezone.now) # 회원가입 날짜
    player_info = models.CharField(max_length=20, blank=True) # 우투우타 등의 정보
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        return "/players/%s/" % urlquote(self.email)

    def get_short_name(self):
        return self.name

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])


class Player(BaseUser):
    """각 선수들에 대한 정보
    경기 성적이 아닌 선수 신상 정보
    AbstractBaseUser 클래스를 상속 받아 수정
    email을 id 값으로 사용
    UserManager도 수정 필요
    """
    team = models.ManyToManyField(Team, blank=True)
    league = models.ManyToManyField(League, blank=True)
    region = models.ForeignKey(Region, null=True)

    def __str__(self):
        return self.email


class GameSchedule(models.Model):

    league = models.ForeignKey(League) # foreignkey를 기준으로 리그별 경기 구별
    game_date = models.DateField(blank=True)
    team = models.CharField(max_length=100, blank=True) # 모델상에서는 데이터를 하나만 가지고 있지만 이후에 form상에서 두개의 팀을 입력할 수 있도록 활용.
    place = models.ForeignKey(GamePlace)

    def __str__(self):
        return self.league.name + " 리그의 "+ str(self.game_date) + " 경기"


class TeamHasLeague(models.Model):
    """리그별 팀 기록
    """
    team = models.ForeignKey(Team)
    league = models.ForeignKey(League)
    win = models.PositiveSmallIntegerField(blank=True, null=True)
    lose = models.PositiveSmallIntegerField(blank=True, null=True)
    draw = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return self.league.name + "에 속한 " + self.team.name + " 팀"


class PitcherHasTeam(models.Model):
    """각 투수별 팀 기록
    """
    player = models.ForeignKey(Player)
    team = models.ForeignKey(Team)
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


class HitterHasTeam(models.Model):
    """각 타자별 팀 기록
    """
    player = models.ForeignKey(Player)
    team = models.ForeignKey(Team)
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


class PitcherHasLeague(models.Model):
    """각 투수별 리그 성적
    """
    player = models.ForeignKey(Player)
    league = models.ForeignKey(League)
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


class HitterHasLeague(models.Model):
    """각 타자별 리그 성적
    """
    player = models.ForeignKey(Player)
    league = models.ForeignKey(League)
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


class GameDetailHitter(models.Model):
    """각 게임 세부 정보 및
    타자 기록
    """
    player = models.ForeignKey(Player)
    game = models.ForeignKey(GameSchedule)
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


class GameDetailPitcher(models.Model):
    """각 게임별 투수 세부 기록
    """
    game = models.ForeignKey(GameSchedule)
    player = models.ForeignKey(Player)
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


