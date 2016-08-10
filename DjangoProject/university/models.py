# coding: utf-8

from django.db import models

class University(models.Model):
    """대학 동아리 팀들이 속한 대학 정보
    """
    name = models.CharField(max_length=20) # 앞단에서 선택가능하도록 
    region = models.CharField(max_length=50) # 대학 선택시 자동으로 입력되게끔
    registration_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class Team(models.Model):
    """각 팀의 기본 정보 모델
    """
    name = models.CharField(max_length=50)
    manager = models.CharField(max_length=20) # 팀 관리자, 처음 생성자 아이디 값 받을 수도
    university = models.ForeignKey(University)
    rate = models.IntegerField() # 승률, 계산해서 들어갈 값
    
    def __str__(self):
        return self.name

class League(models.Model):
    """각 리그별 기본 정보 
    각 팀 매니저가 생성 가능
    """
    name = models.CharField(max_length=100)
    start_date = models.DateField(auto_now_add=True)
    finish_date = models.DateField() # 리그 기간에 대한 정보
   
    def __str__(self):
        return self.name 

class Player(models.Model):
    """각 선수들에 대한 정보 
    User와는 별개로 회원 가입 후에 별도로 입력 받음 
    경기 성적이 아닌 선수 신상 정보 
    """
    name = models.CharField(max_length=20)
    age = models.PositiveSmallIntegerField() # 나이 
    main_position = models.CharField(max_length=20) # 주 포지션 
    height = models.PositiveSmallIntegerField() # 선수 키 
    weight = models.PositiveSmallIntegerField() # 선수 몸무게 
    start_date = models.DateField() # 선수 경력 시작 일 기준, 사용자가 입력
    player_info = models.CharField(max_length=20) # 우투우타 등의 정보
    team = models.ForeignKey(Team)
    university = models.ForeignKey(University)

    def __str__(self):
        return self.name

class GamePlace(models.Model):
    """게임이 진행되는 경기장 정보 
    데이터 입력해놓고 사용자가 선택하는 방식
    """
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100) # 경기장 주소
    # 추후에 칼럼 추가 예정 

    def __str__(self):
        return self.name

class GameSchedule(models.Model):
    """경기 일정 각 모든 리그 전체
    """
    league = models.ForeignKey(League)
    game_date = models.DateField() # 게임 날짜
    team = models.CharField(max_length=100) # 게임을 진행하는 2 팀 
    place = models.ForeignKey(GamePlace)

    def __str__(self):
        return self.league.name + " 리그의 "+ str(self.game_date) + " 경기"

class TeamHasLeague(models.Model):
    """리그별 팀 기록 
    """
    team = models.ForeignKey(Team)
    league = models.ForeignKey(League)
    win = models.PositiveSmallIntegerField()
    lose = models.PositiveSmallIntegerField()
    draw = models.PositiveSmallIntegerField()
    
    def __str__(self):
        return self.league.name + "에 속한 " + self.team.name + " 팀"

class PitcherHasTeam(models.Model):
    """각 투수별 팀 기록 
    """
    player = models.ForeignKey(Player)
    team = models.ForeignKey(Team)
    game = models.PositiveSmallIntegerField() # 등판 경기 수
    win = models.PositiveSmallIntegerField() # 승리  
    lose = models.PositiveSmallIntegerField() # 패배
    ininig = models.PositiveSmallIntegerField() # 이닝 수
    save = models.PositiveSmallIntegerField() # 세이브 
    hold = models.PositiveSmallIntegerField() # 홀드 
    hit = models.PositiveSmallIntegerField() # 피안타 갯수
    HR = models.PositiveSmallIntegerField() # 피홈런 갯수 
    run = models.PositiveSmallIntegerField() # 실점
    BB = models.PositiveSmallIntegerField() # 볼넷 
    HBP = models.PositiveSmallIntegerField() # 사구
    K = models.PositiveSmallIntegerField() # 삼진
    pitches = models.PositiveSmallIntegerField() # 던진 공 갯수 

    def __str__(self):
        return self.team.name +" 팀의 " + self.player.name 

class HitterHasTeam(models.Model):
    """각 타자별 팀 기록 
    """
    player = models.ForeignKey(Player)
    team = models.ForeignKey(Team)
    AB = models.PositiveSmallIntegerField() # 타수
    H = models.PositiveSmallIntegerField() # 안타
    double = models.PositiveSmallIntegerField() # 2루타
    triple = models.PositiveSmallIntegerField() # 3루타
    HR = models.PositiveSmallIntegerField() # 홈런
    R = models.PositiveSmallIntegerField() # 득점
    RBI = models.PositiveSmallIntegerField() # 타점
    BB = models.PositiveSmallIntegerField() # 볼넷
    HBP = models.PositiveSmallIntegerField() # 사구
    K = models.PositiveSmallIntegerField() # 삼진
    # TPA 타석은 타수에서 볼넷과 사구를 뺀 값
    SB = models.PositiveSmallIntegerField() # 도루 성공
    CS = models.PositiveSmallIntegerField() # 도루 실패
    # 총 도루 시도는 도루성공 + 도루 실패 
    game = models.PositiveSmallIntegerField() # 출장 게임 수 

    def __str__(self):
        return self.team.name +" 팀의 " + self.player.name 
    
class PitcherHasLeague(models.Model):
    """각 투수별 리그 성적
    """
    player = models.ForeignKey(Player)
    league = models.ForeignKey(League)
    game = models.PositiveSmallIntegerField() # 등판 경기 수
    win = models.PositiveSmallIntegerField() # 승리  
    lose = models.PositiveSmallIntegerField() # 패배
    ininig = models.PositiveSmallIntegerField() # 이닝 수
    save = models.PositiveSmallIntegerField() # 세이브 
    hold = models.PositiveSmallIntegerField() # 홀드 
    hit = models.PositiveSmallIntegerField() # 피안타 갯수
    HR = models.PositiveSmallIntegerField() # 피홈런 갯수 
    run = models.PositiveSmallIntegerField() # 실점
    BB = models.PositiveSmallIntegerField() # 볼넷 
    HBP = models.PositiveSmallIntegerField() # 사구
    K = models.PositiveSmallIntegerField() # 삼진
    pitches = models.PositiveSmallIntegerField() # 던진 공 갯수 

    def __str__(self):
        return self.league.name +" 리그의 " + self.player.name 

class HitterHasLeague(models.Model):
    """각 타자별 리그 성적 
    """
    player = models.ForeignKey(Player)
    league = models.ForeignKey(League)
    AB = models.PositiveSmallIntegerField() # 타수
    H = models.PositiveSmallIntegerField() # 안타
    double = models.PositiveSmallIntegerField() # 2루타
    triple = models.PositiveSmallIntegerField() # 3루타
    HR = models.PositiveSmallIntegerField() # 홈런
    R = models.PositiveSmallIntegerField() # 득점
    RBI = models.PositiveSmallIntegerField() # 타점
    BB = models.PositiveSmallIntegerField() # 볼넷
    HBP = models.PositiveSmallIntegerField() # 사구
    K = models.PositiveSmallIntegerField() # 삼진
    # TPA 타석은 타수에서 볼넷과 사구를 뺀 값
    SB = models.PositiveSmallIntegerField() # 도루 성공
    CS = models.PositiveSmallIntegerField() # 도루 실패
    # 총 도루 시도는 도루성공 + 도루 실패 
    game = models.PositiveSmallIntegerField() # 출장 게임 수 

    def __str__(self):
        return self.league.name +" 리그의 " + self.player.name 

class GameDetailHitter(models.Model):
    """각 게임 세부 정보 및 
    타자 기록 
    """
    player = models.ForeignKey(Player)
    game = models.ForeignKey(GameSchedule)
    ininig_1 = models.CharField(max_length=100) # 각 이닝 정보 
    ininig_2 = models.CharField(max_length=100) # 각 이닝 정보 
    ininig_3 = models.CharField(max_length=100) # 각 이닝 정보 
    ininig_4 = models.CharField(max_length=100) # 각 이닝 정보 
    ininig_5 = models.CharField(max_length=100) # 각 이닝 정보 
    ininig_6 = models.CharField(max_length=100) # 각 이닝 정보 
    ininig_7 = models.CharField(max_length=100) # 각 이닝 정보 
    ininig_8 = models.CharField(max_length=100) # 각 이닝 정보 
    ininig_9 = models.CharField(max_length=100) # 각 이닝 정보
    AB = models.PositiveSmallIntegerField() # 타수 
    hit = models.PositiveSmallIntegerField() # 안타 
    run = models.PositiveSmallIntegerField() # 득점
    RBI = models.PositiveSmallIntegerField() # 타점
    SB = models.PositiveSmallIntegerField() # 도루 성공
    CS = models.PositiveSmallIntegerField() # 도루 실패 
    BB = models.PositiveSmallIntegerField() # 볼넷
    HBP = models.PositiveSmallIntegerField() # 사구 
    # TPA(타석 수) = AB + BB + HBP
    # 총 도루시도 = SB + CS 
    # AVG = H / TPA

    def __str__(self):
        return str(self.game.game_date) + " 경기 " + self.player.name + "선수 성적"

class GameDetailPitcher(models.Model):
    """각 게임별 투수 세부 기록 
    """
    game = models.ForeignKey(GameSchedule)
    player = models.ForeignKey(Player)
    win = models.BooleanField() # 승패 
    save = models.BooleanField() # 세이브 여부
    hold = models.BooleanField() # 홀드 여부 
    HR = models.PositiveSmallIntegerField() # 피홈런
    hit = models.PositiveSmallIntegerField() # 피안타 
    K = models.PositiveSmallIntegerField() # 탈삼진 
    run = models.PositiveSmallIntegerField() # 실점
    BB = models.PositiveSmallIntegerField() # 볼넷
    HBP = models.PositiveSmallIntegerField() # 사구 
    pitches = models.PositiveSmallIntegerField() # 공갯수 
    
    def __str__(self):
        return str(self.game.game_date) + " 경기 " + self.player.name  + "선수 성적"


