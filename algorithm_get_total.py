import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "final_pjt.settings")
## 프로젝트를 사용할 수 있도록 환경 생성
import django

django.setup()

from algorithm.models import *

## python파일의 위치
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


br = BJData_br.objects.all()
si = BJData_si.objects.all()
go = BJData_go.objects.all()
pl = BJData_pl.objects.all()
di = BJData_di.objects.all()
ru = BJData_ru.objects.all()
total = BJData_total.objects.all()


total_queryset = total.union(br).union(si).union(go).union(pl).union(di).union(ru)

for q in total_queryset:
    print(q.number, q.title)
    BJData_total.objects.create(level=q.level, number=q.number, title=q.title, tags=q.tags)