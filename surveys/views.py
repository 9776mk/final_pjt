from django.shortcuts import render, redirect
from .models import *
from .forms import *

# Create your views here.
def index(request):
    # 1. 코딩 시작 나이
    ages = Survey.objects.all().values_list("start_age", flat=True)
    ages_dict = {
        "10대": 0,
        "20대": 0,
        "30대": 0,
        "40대": 0,
        "50대": 0,
        "60대": 0,
        "70대 이상": 0,
    }

    for age in ages:
        ages_dict[age] += 1
    total_people_cnt = len(ages)  # 설문에 응답한 총 사람의 수

    for k, v in ages_dict.items():
        ages_dict[k] = int(round(v / total_people_cnt, 2) * 100)

    sorted_ages = sorted(ages_dict.items(), key=lambda item: item[1], reverse=True)
    print(sorted_ages)

    # 2. 코딩 경력
    careers = Survey.objects.all().values_list("career", flat=True)
    careers_dict = {
        "1년 미만": 0,
        "1년 이상": 0,
        "2년 이상": 0,
        "3년 이상": 0,
        "4년 이상": 0,
        "5년 이상": 0,
        "시니어": 0,
    }

    for career in careers:
        careers_dict[career] += 1

    for k, v in careers_dict.items():
        careers_dict[k] = int(round(v / total_people_cnt, 2) * 100)

    sorted_careers = sorted(
        careers_dict.items(), key=lambda item: item[1], reverse=True
    )
    print(sorted_careers)

    # 3. 개발자 유형
    developers = Survey.objects.all().values_list("developer_type", flat=True)
    developers_dict = {
        "풀스택 개발자": 0,
        "백엔드 개발자": 0,
        "프론트엔드 개발자": 0,
        "기타": 0,
    }

    for developer in developers:
        developers_dict[developer] += 1

    for k, v in developers_dict.items():
        developers_dict[k] = int(round(v / total_people_cnt, 2) * 100)

    sorted_developers = sorted(
        developers_dict.items(), key=lambda item: item[1], reverse=True
    )
    print(sorted_developers)

    # 4. 배우고 싶은 언어
    d_langs = Survey.objects.all().values_list("desired_language", flat=True)
    d_langs_dict = {
        "Python": 0,
        "C": 0,
        "Java": 0,
        "JavaScript": 0,
        "HTML/CSS": 0,
        "기타": 0,
    }

    for lang in d_langs:
        d_langs_dict[lang] += 1

    for k, v in d_langs_dict.items():
        d_langs_dict[k] = int(round(v / total_people_cnt, 2) * 100)

    sorted_d_langs = sorted(
        d_langs_dict.items(), key=lambda item: item[1], reverse=True
    )
    print(sorted_d_langs)

    # 5. 가장 많이 사용하는 언어
    u_langs = Survey.objects.all().values_list("most_using_language", flat=True)
    u_langs_dict = {
        "Python": 0,
        "C": 0,
        "Java": 0,
        "JavaScript": 0,
        "HTML/CSS": 0,
        "기타": 0,
    }

    for lang in u_langs:
        u_langs_dict[lang] += 1

    for k, v in u_langs_dict.items():
        u_langs_dict[k] = int(round(v / total_people_cnt, 2) * 100)

    sorted_u_langs = sorted(
        u_langs_dict.items(), key=lambda item: item[1], reverse=True
    )
    print(sorted_u_langs)

    # 6. 코딩을 배운 방법
    methods = Survey.objects.all().values_list("how_to_learn", flat=True)
    methods_dict = {
        "학교": 0,
        "책": 0,
        "온라인 강의": 0,
        "코딩 부트캠프": 0,
        "기타 자료 (동영상, 블로그 등)": 0,
        "기타": 0,
    }

    for method in methods:
        methods_dict[method] += 1

    for k, v in methods_dict.items():
        methods_dict[k] = int(round(v / total_people_cnt, 2) * 100)

    sorted_methods = sorted(
        methods_dict.items(), key=lambda item: item[1], reverse=True
    )
    print(sorted_methods)

    # 7. 하루 평균 학습 시간
    hours = Survey.objects.all().values_list("daily_learning_hours", flat=True)
    hours_dict = {
        "1시간 미만": 0,
        "1시간 이상 3시간 미만": 0,
        "3시간 이상 5시간 미만": 0,
        "5시간 이상 10시간 미만": 0,
        "10시간 이상": 0,
    }

    for hour in hours:
        hours_dict[hour] += 1

    for k, v in hours_dict.items():
        hours_dict[k] = int(round(v / total_people_cnt, 2) * 100)

    sorted_hours = sorted(hours_dict.items(), key=lambda item: item[1], reverse=True)
    print(sorted_hours)

    # 9. 학위
    degrees = Survey.objects.all().values_list("degree", flat=True)
    degrees_dict = {
        "고졸": 0,
        "전문학사": 0,
        "학사": 0,
        "석사": 0,
        "박사": 0,
    }

    for degree in degrees:
        degrees_dict[degree] += 1

    for k, v in degrees_dict.items():
        degrees_dict[k] = int(round(v / total_people_cnt, 2) * 100)

    sorted_degrees = sorted(
        degrees_dict.items(), key=lambda item: item[1], reverse=True
    )
    print(sorted_degrees)

    # 10. 성별
    genders = Survey.objects.all().values_list("gender", flat=True)
    genders_dict = {
        "여성": 0,
        "남성": 0,
        "제3의 성": 0,
    }

    for gender in genders:
        genders_dict[gender] += 1

    for k, v in genders_dict.items():
        genders_dict[k] = int(round(v / total_people_cnt, 2) * 100)

    sorted_genders = sorted(
        genders_dict.items(), key=lambda item: item[1], reverse=True
    )
    print(sorted_genders)

    # 11. MBTI
    mbtis = Survey.objects.all().values_list("mbti", flat=True)
    mbtis_dict = {
        "ISTJ": 0,
        "ISFJ": 0,
        "INFJ": 0,
        "INTJ": 0,
        "ISTP": 0,
        "ISFP": 0,
        "INFP": 0,
        "INTP": 0,
        "ESTJ": 0,
        "ESFJ": 0,
        "ENFJ": 0,
        "ENTJ": 0,
        "ESTP": 0,
        "ESFP": 0,
        "ENFP": 0,
        "ENTP": 0,
    }

    for mbti in mbtis:
        mbtis_dict[mbti] = mbtis_dict.get(mbti, 0) + 1

    for k, v in mbtis_dict.items():
        mbtis_dict[k] = int(round(v / total_people_cnt, 2) * 100)

    sorted_mbtis = sorted(mbtis_dict.items(), key=lambda item: item[1], reverse=True)
    print(sorted_mbtis)

    context = {
        "sorted_ages": sorted_ages,
        "sorted_careers": sorted_careers,
        "sorted_developers": sorted_developers,
        "sorted_d_langs": sorted_d_langs,
        "sorted_u_langs": sorted_u_langs,
        "sorted_methods": sorted_methods,
        "sorted_hours": sorted_hours,
        "sorted_degrees": sorted_degrees,
        "sorted_genders": sorted_genders,
        "sorted_mbtis": sorted_mbtis,
    }

    return render(request, "surveys/index.html", context)


def create(request):
    if request.method == "POST":
        survey_form = SurveyForm(request.POST)
        print(survey_form.is_valid())

        if survey_form.is_valid():
            survey_form.save()
            return redirect("home")

    else:
        survey_form = SurveyForm()

    context = {
        "survey_form": survey_form,
    }

    return render(request, "surveys/create.html", context)
