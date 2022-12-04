import json
import os

## Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로를 등록
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "final_pjt.settings")
## 프로젝트를 사용할 수 있도록 환경 생성
import django

django.setup()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

from algorithm.models import BJData

with open(os.path.join(BASE_DIR, "problems.json"), "r", encoding="UTF-8") as json_file:
    json_file = json.load(json_file)

# json_file['변수명']['인덱스']로 확인 가능


len_ = len(json_file["level"])


for i in range(len_):
    level = json_file["level"][i]
    number = json_file["number"][i]
    title = json_file["title"][i]
    tags = json_file["tags"][i]

    if __name__ == "__main__":
        BJData(level=level, number=number, title=title, tags=tags).save()


# for k, v in json_file.items():
#     print(k, v)
