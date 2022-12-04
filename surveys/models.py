from django.db import models

# Create your models here.
# https://insights.stackoverflow.com/survey/2021
class Survey(models.Model):
    # 앞: DB에 저장되는 값, 뒤: admin이나 form에서 표시하는 값
    # 코딩 시작 나이
    START_AGE = (
        ('10대', '10대'), ('20대', '20대'), ('30대', '30대'), ('40대', '40대'),
        ('50대', '50대'), ('60대', '60대'), ('70살 이상', '70살 이상'),
    )
    start_age = models.CharField(max_length=10, choices=START_AGE)

    # 코딩 경력
    CAREER = (
        ('1년 미만', '1년 미만'), ('1년 이상', '1년 이상'), ('2년 이상', '2년 이상'), ('3년 이상', '3년 이상'),
        ('4년 이상', '4년 이상'), ('5년 이상', '5년 이상'), ('시니어', '시니어'),
    )
    career = models.CharField(max_length=10, choices=CAREER)

    # 개발자 유형
    DEVELOPER_TYPE = (
        ('풀스택 개발자', '풀스택 개발자'),
        ('백엔드 개발자', '백엔드 개발자'),
        ('프론트엔드 개발자', '프론트엔드 개발자'),
        ('기타', '기타'),
    )
    developer_type = models.CharField(max_length=10, choices=DEVELOPER_TYPE)

    # 배우고 싶은 언어
    DESIRED_LANGUAGE = (
        ('Python', 'Python'), ('C', 'C'), ('Java', 'Java'),
        ('JavaScript', 'JavaScript'), ('HTML/CSS', 'HTML/CSS'), ('기타', '기타'),
        # 프레임워크도?
    )
    desired_language = models.CharField(max_length=10, choices=DESIRED_LANGUAGE)

    # 가장 많이 사용하는 언어
    MOST_USING_LANGUAGE = (
        ('Python', 'Python'), ('C', 'C'), ('Java', 'Java'),
        ('JavaScript', 'JavaScript'), ('HTML/CSS', 'HTML/CSS'), ('기타', '기타'),
    )
    most_using_language = models.CharField(max_length=10, choices=MOST_USING_LANGUAGE)

    # 코딩을 배운 방법
    HOW_TO_LEARN = (
        ('학교', '학교'), ('책', '책'),
        ('코딩 부트캠프', '코딩 부트캠프'), ('온라인 강의', '온라인 강의'),
        ('기타 자료 (동영상, 블로그 등)', '기타 자료 (동영상, 블로그 등)'), ('기타', '기타'),
    )
    how_to_learn = models.CharField(max_length=20, choices=HOW_TO_LEARN)

    # 하루 평균 학습 시간
    DAILY_LEARNING_HOURS = (
        ('1시간 미만', '1시간 미만'), 
        ('1시간 이상 3시간 미만', '1시간 이상 3시간 미만'), 
        ('3시간 이상 5시간 미만', '3시간 이상 5시간 미만'),
        ('5시간 이상 10시간 미만', '5시간 이상 10시간 미만'),
        ('10시간 이상', '10시간 이상'),
    )
    daily_learning_hours = models.CharField(max_length=20, choices=DAILY_LEARNING_HOURS)

    # 학력
    EDUCATION = (
        ('중졸 이하', '중졸 이하'), ('고졸', '고졸'), 
        ('전문대졸', '전문대졸'), ('대졸 이상', '대졸 이상'),
    )
    education = models.CharField(max_length=20, choices=EDUCATION)

    # 학위
    DEGREE = (
        ('없음', '없음'), ('전문학사', '전문학사'), 
        ('학사', '학사'), ('석사', '석사'), ('박사', '박사'),
    )
    degree = models.CharField(max_length=20, choices=DEGREE)

    # 성별
    GENDER = (
        ('여성', '여성'), ('남성', '남성'), ('제3의 성', '제3의 성')
    )
    gender = models.CharField(max_length=20, choices=GENDER)

    # MBTI
    MBTI = (
        ('ISTJ', 'ISTJ'), ('ISFJ', 'ISFJ'), ('INFJ', 'INFJ'), ('INTJ', 'INTJ'),
        ('ISTP', 'ISTP'), ('ISFP', 'ISFP'), ('INFP', 'INFP'), ('INTP', 'INTP'),
        ('ESTJ', 'ESTJ'), ('ESFJ', 'ESFJ'), ('ENFJ', 'ENFJ'), ('ENTJ', 'ENTJ'),
        ('ESTP', 'ESTP'), ('ESFP', 'ESFP'), ('ENFP', 'ENFP'), ('ENTP', 'ENTP'),
    )
    mbti = models.CharField(blank=True, max_length=4, choices=MBTI)