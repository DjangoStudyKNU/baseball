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

class Game_place(models.Model):
    """게임이 진행되는 경기장 정보 
    데이터 입력해놓고 사용자가 선택하는 방식
    """
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100) # 경기장 주소
    # 추후에 칼럼 추가 예정 

    def __str__(self):
        return self.name

    



