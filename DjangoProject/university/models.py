# coding: utf-8

from django.utils import timezone 
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail

class University(models.Model):
    """대학 동아리 팀들이 속한 대학 정보
    대학별 선수 기록 필터 필요?
    """
    name = models.CharField(max_length=20) # 앞단에서 선택가능하도록 
    region = models.CharField(max_length=50, blank=True) # 대학 선택시 자동으로 입력되게끔
    registration_date = models.DateField(auto_now_add=True)
    logo = models.ImageField(blank=True)

    def __str__(self):
        return self.name

class UniversityTeam(models.Model):
    """각 팀의 기본 정보 모델
    """
    name = models.CharField(max_length=50)
    manager = models.CharField(max_length=20, blank=True) # 팀 관리자, 처음 생성자 아이디 값 받을 수도
    university = models.ForeignKey(University)
    rate = models.DecimalField(max_digits=20,decimal_places=4, blank=True, null=True) # 승률, 계산해서 들어갈 값
    logo = models.ImageField(blank=True)
    
    def __str__(self):
        return self.name

class UniversityLeague(models.Model):
    """각 리그별 기본 정보 
    각 팀 매니저가 생성 가능
    """
    name = models.CharField(max_length=100)
    start_date = models.DateField(auto_now_add=True)
    finish_date = models.DateField(blank=True, null=True) # 리그 기간에 대한 정보
    logo = models.ImageField(blank=True)
    
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


class Player(AbstractBaseUser, PermissionsMixin):
    """각 선수(유저)들에 대한 정보 
    경기 성적이 아닌 선수 신상 정보 
    AbstractBaseUser 클래스를 상속 받아 수정
    email을 id 값으로 사용
    UserManager도 수정 필요
    Permission 관리 필요 
    """
    email = models.EmailField(_('email address'), unique=True, max_length=255)
    photo = models.ImageField(blank=True)
    name = models.CharField(_('name'), max_length=30, blank=True)
    age = models.PositiveSmallIntegerField(blank=True, null=True) # 나이 
    main_position = models.CharField(max_length=20, blank=True) # 주 포지션 
    height = models.PositiveSmallIntegerField(blank=True, null=True) # 선수 키 
    weight = models.PositiveSmallIntegerField(blank=True, null=True) # 선수 몸무게 
    date_joined = models.DateTimeField(default=timezone.now) # 회원가입 날짜 
    player_info = models.CharField(max_length=20, blank=True) # 우투우타 등의 정보
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    
    # university에서 쓸 부분
    university_team = models.ManyToManyField(UniversityTeam, blank=True)
    university_league = models.ManyToManyField(UniversityLeague, blank=True)
    university = models.ForeignKey(University, blank=True, null=True)
    
    # amatuer에서 쓸 부분 
    amateur_team = models.ManyToManyField("amateur.AmateurTeam", blank=True)
    amateur_league = models.ManyToManyField("amateur.AmateurLeague", blank=True)
    region = models.ForeignKey("amateur.Region", blank=True, null=True)
    
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

    def __str__(self):
        return self.email

class UniversityGamePlace(models.Model):
    """게임이 진행되는 경기장 정보 
    데이터 입력해놓고 사용자가 선택하는 방식
    """
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100, blank=True) # 경기장 주소
    # 추후에 칼럼 추가 예정 

    def __str__(self):
        return self.name

class UniversityGameSchedule(models.Model):
    """경기 일정 각 모든 리그 전체
    """
    league = models.ForeignKey(UniversityLeague)
    game_date = models.DateField(blank=True) # 게임 날짜
    team = models.CharField(max_length=100, blank=True) # 게임을 진행하는 2 팀 
    place = models.ForeignKey(UniversityGamePlace)

    def __str__(self):
        return self.league.name + " 리그의 "+ str(self.game_date) + " 경기"

class UniversityTeamHasLeague(models.Model):
    """리그별 팀 기록 
    """
    team = models.ForeignKey(UniversityTeam)
    league = models.ForeignKey(UniversityLeague)
    win = models.PositiveSmallIntegerField(blank=True, null=True)
    lose = models.PositiveSmallIntegerField(blank=True, null=True)
    draw = models.PositiveSmallIntegerField(blank=True, null=True)
    
    def __str__(self):
        return self.league.name + "에 속한 " + self.team.name + " 팀"

class UniversityPitcherHasTeam(models.Model):
    """각 투수별 팀 기록 
    """
    player = models.ForeignKey(Player)
    team = models.ForeignKey(UniversityTeam)
    game = models.PositiveSmallIntegerField(blank=True, null=True) # 등판 경기 수
    win = models.PositiveSmallIntegerField(blank=True, null=True) # 승리  
    lose = models.PositiveSmallIntegerField(blank=True, null=True) # 패배
    ininig = models.PositiveSmallIntegerField(blank=True, null=True) # 이닝 수
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

class UniversityHitterHasTeam(models.Model):
    """각 타자별 팀 기록 
    """
    player = models.ForeignKey(Player)
    team = models.ForeignKey(UniversityTeam)
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
    # TPA 타석은 타수에서 볼넷과 사구를 뺀 값
    SB = models.PositiveSmallIntegerField(blank=True, null=True) # 도루 성공
    CS = models.PositiveSmallIntegerField(blank=True, null=True) # 도루 실패
    # 총 도루 시도는 도루성공 + 도루 실패 
    game = models.PositiveSmallIntegerField(blank=True, null=True) # 출장 게임 수 

    def __str__(self):
        return self.team.name +" 팀의 " + self.player.name 
    
class UniversityPitcherHasLeague(models.Model):
    """각 투수별 리그 성적
    """
    player = models.ForeignKey(Player)
    league = models.ForeignKey(UniversityLeague)
    game = models.PositiveSmallIntegerField(blank=True, null=True) # 등판 경기 수
    win = models.PositiveSmallIntegerField(blank=True, null=True) # 승리  
    lose = models.PositiveSmallIntegerField(blank=True, null=True) # 패배
    ininig = models.PositiveSmallIntegerField(blank=True, null=True) # 이닝 수
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

class UniversityHitterHasLeague(models.Model):
    """각 타자별 리그 성적 
    """
    player = models.ForeignKey(Player)
    league = models.ForeignKey(UniversityLeague)
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
    # TPA 타석은 타수에서 볼넷과 사구를 뺀 값
    SB = models.PositiveSmallIntegerField(blank=True, null=True) # 도루 성공
    CS = models.PositiveSmallIntegerField(blank=True, null=True) # 도루 실패
    # 총 도루 시도는 도루성공 + 도루 실패 
    game = models.PositiveSmallIntegerField(blank=True, null=True) # 출장 게임 수 

    def __str__(self):
        return self.league.name +" 리그의 " + self.player.name 

class UniversityGameDetailHitter(models.Model):
    """각 게임 세부 정보 및 
    타자 기록 
    """
    player = models.ForeignKey(Player)
    game = models.ForeignKey(UniversityGameSchedule)
    ininig_1 = models.CharField(max_length=100, blank=True) # 각 이닝 정보 
    ininig_2 = models.CharField(max_length=100, blank=True) # 각 이닝 정보 
    ininig_3 = models.CharField(max_length=100, blank=True) # 각 이닝 정보 
    ininig_4 = models.CharField(max_length=100, blank=True) # 각 이닝 정보 
    ininig_5 = models.CharField(max_length=100, blank=True) # 각 이닝 정보 
    ininig_6 = models.CharField(max_length=100, blank=True) # 각 이닝 정보 
    ininig_7 = models.CharField(max_length=100, blank=True) # 각 이닝 정보 
    ininig_8 = models.CharField(max_length=100, blank=True) # 각 이닝 정보 
    ininig_9 = models.CharField(max_length=100, blank=True) # 각 이닝 정보
    AB = models.PositiveSmallIntegerField(blank=True, null=True) # 타수 
    hit = models.PositiveSmallIntegerField(blank=True, null=True) # 안타 
    run = models.PositiveSmallIntegerField(blank=True, null=True) # 득점
    RBI = models.PositiveSmallIntegerField(blank=True, null=True) # 타점
    SB = models.PositiveSmallIntegerField(blank=True, null=True) # 도루 성공
    CS = models.PositiveSmallIntegerField(blank=True, null=True) # 도루 실패 
    BB = models.PositiveSmallIntegerField(blank=True, null=True) # 볼넷
    HBP = models.PositiveSmallIntegerField(blank=True, null=True) # 사구 
    # TPA(타석 수) = AB + BB + HBP
    # 총 도루시도 = SB + CS 
    # AVG = H / TPA

    def __str__(self):
        return str(self.game.game_date) + " 경기 " + self.player.name + "선수 성적"

class UniversityGameDetailPitcher(models.Model):
    """각 게임별 투수 세부 기록 
    """
    game = models.ForeignKey(UniversityGameSchedule)
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


