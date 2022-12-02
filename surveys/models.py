from django.db import models

# Create your models here.
# https://insights.stackoverflow.com/survey/2021
class Survey(models.Model):
    # 앞: DB에 저장되는 값, 뒤: admin이나 form에서 표시하는 값
    # 코딩 시작 나이
    START_AGE = (
        ('10', '10대'), ('20', '20대'), ('30', '30대'), ('40', '40대'),
        ('50', '50대'), ('60', '60대'), ('70', '70살 이상'),
    )
    start_age = models.CharField(max_length=10, choices=START_AGE)

    # 코딩 경력
    CAREER = (
        ('lt1', '1년 미만'), ('ge1', '1년 이상'), ('ge2', '2년 이상'), ('ge3', '3년 이상'),
        ('ge4', '4년 이상'), ('ge5', '5년 이상'), ('senior', '시니어'),
    )
    career = models.CharField(max_length=10, choices=CAREER)

    # 개발자 유형
    DEVELOPER_TYPE = (
        ('full-stack', '풀스택 개발자'),
        ('back-end', '백엔드 개발자'),
        ('front-end', '프론트엔드 개발자'),
        ('etc', '기타'),
    )
    developer_type = models.CharField(max_length=10, choices=DEVELOPER_TYPE)

    # 배우고 싶은 언어
    DESIRED_LANGUAGE = (
        ('python', 'Python'), ('c', 'C'), ('java', 'Java'),
        ('javascript', 'JavaScript'), ('html_css', 'HTML/CSS'), ('etc', '기타'),
        # 프레임워크도?
    )
    desired_language = models.CharField(max_length=10, choices=DESIRED_LANGUAGE)

    # 가장 많이 사용하는 언어
    MOST_USING_LANGUAGE = (
        ('python', 'Python'), ('c', 'C'), ('java', 'Java'),
        ('javascript', 'JavaScript'), ('html_css', 'HTML/CSS'), ('etc', '기타'),
    )
    most_using_language = models.CharField(max_length=10, choices=MOST_USING_LANGUAGE)

    # 코딩을 배운 방법
    HOW_TO_LEARN = (
        ('school', '학교'), ('books', '책'),
        ('coding_bootcamp', '코딩 부트캠프'), ('online_courses', '온라인 강의'),
        ('other_resourses', '기타 자료 (동영상, 블로그 등)'), ('etc', '기타'),
    )
    how_to_learn = models.CharField(max_length=20, choices=HOW_TO_LEARN)

    # 하루 평균 학습 시간
    DAILY_LEARNING_HOURS = (
        ('lt1', '1시간 미만'), 
        ('ge1-lt3', '1시간 이상 3시간 미만'), 
        ('ge3-lt5', '3시간 이상 5시간 미만'),
        ('ge5-lt10', '5시간 이상 10시간 미만'),
        ('ge10', '10시간 이상'),
    )
    daily_learning_hours = models.CharField(max_length=20, choices=DAILY_LEARNING_HOURS)

    # 학력
    EDUCATION = (
        ('middle_school', '중졸 이하'), ('high_school', '고졸'), 
        ('junior_college', '전문대 졸'), ('university', '대졸 이상'),
    )
    education = models.CharField(max_length=20, choices=EDUCATION)

    # 학위
    DEGREE = (
        ('none', '없음'), ('associate', '전문학사'), 
        ('bachelor', '학사'), ('master', '석사'), ('doctor', '박사'),
    )
    degree = models.CharField(max_length=20, choices=DEGREE)

    # 성별
    GENDER = (
        ('female', '여성'), ('male', '남성'), ('third-gender', '제3의 성')
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