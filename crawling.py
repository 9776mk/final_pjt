from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time, os, json

from selenium.webdriver.common.keys import Keys

## Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로를 등록
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "final_pjt.settings")
## 프로젝트를 사용할 수 있도록 환경 생성
import django

django.setup()

from algorithm.models import *

## python파일의 위치
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# options = webdriver.ChromeOptions()
# options.add_experimental_option("excludeSwitches", ["enable-logging"])
# browser = webdriver.Chrome(options=options)

page = {
    # 브론즈
    1: 3,
    2: 4,
    3: 11,
    4: 16,
    5: 13,
    # 실버
    6: 13,
    7: 15,
    8: 15,
    9: 16,
    10: 15,
    # 골드
    11: 18,
    12: 20,
    13: 20,
    14: 18,
    15: 17,
    # 플레
    16: 18,
    17: 18,
    18: 19,
    19: 18,
    20: 15,
    # 다이아
    21: 15,
    22: 14,
    23: 10,
    24: 8,
    25: 6,
    # 루비
    26: 5,
    27: 3,
    28: 2,
    29: 1,
    30: 1,
}

# for i in range(1, 31):
for i in range(1, 2):
    temp = {}
    result = {}
    level_ = []
    num_ = []
    title_ = []
    tags_list = []

    driver.refresh()
    v = page[i]
    for j in range(1, 2):
        # for j in range(1, int(v) + 1):
        print(f"{i}레벨 {j}페이지 시작")
        URL = f"https://solved.ac/problems/level/{i}?page={j}"
        driver.get(url=URL)
        # if j == 1 or j == int(v) + 1:
        driver.refresh()
        driver.implicitly_wait(1)
        time.sleep(1)

        c = driver.find_elements(By.CLASS_NAME, "css-gv0s7n")
        count = len(c)
        print(f"len: {count}")
        # level = i
        for lev in range(1, count + 1):
            level_.append(i)
        print(level_)
        # 문제 번호
        # 한 페이지에 최대 50문제 1~50까지
        # 첫 번째 //*[@id="__next"]/div/div[4]/div[2]/div[1]/table/tbody/tr[5]/td[1]/div/div/div/span/a/span
        # 50 번째 //*[@id="__next"]/div/div[4]/div[2]/div[1]/table/tbody/tr[50]/td[1]/div/div/div/span/a/span

        # url_ = []
        for k in range(1, count + 1):
            prob_num = driver.find_elements(
                By.XPATH,
                f'//*[@id="__next"]/div/div[4]/div[2]/div[1]/table/tbody/tr[{k}]/td[1]/div/div/div/span/a/span',
            )
            for number in prob_num:
                num_.append(number.text)
        print(num_)
        #     # url

        #     url_set = driver.find_elements(By.CLASS_NAME, "css-q9j30p")
        #     status = 0
        #     for i in url_set:
        #         if status % 2 == 0:
        #             url_.append(i.get_attribute("href"))
        #         status += 1

        # print(url_)
        # print(len(url_))
        # print(num_)
        # print(len(num_))  # 번호
        # title
        # 첫 번째 //*[@id="__next"]/div/div[4]/div[2]/div[1]/table/tbody/tr[1]/td[2]/span/div/div[1]/span[1]/div/a/span

        for m in range(1, count + 1):
            title = driver.find_elements(
                By.XPATH,
                f'//*[@id="__next"]/div/div[4]/div[2]/div[1]/table/tbody/tr[{m}]/td[2]/span/div/div[1]/span[1]/div/a/span',
            )
            for value in title:
                # print(value.text)
                title_.append(value.text)

        # print(len(title_))
        print(title_)

        for_category = driver.find_elements(By.CLASS_NAME, "css-gv0s7n")
        for n in for_category:
            li = []
            # i.click() element not interactable 에러 발생
            n.send_keys(Keys.ENTER)
            time.sleep(2)  # 이거 안기다리면 오류남
            tags = driver.find_elements(By.CLASS_NAME, "css-1rqtlpb")
            if len(tags) > 1:  # 태그 여러개
                for t in tags:
                    # print(t.text)
                    # print(t.text.lstrip("#"))
                    li.append(t.text.lstrip("#"))
            elif len(tags) == 1:  # 한개
                tags = driver.find_element(By.CLASS_NAME, "css-1rqtlpb")
                # print(tags.text)
                li.append(tags.text.lstrip("#"))
                # print(li)
            else:  # 태그 없을 때
                pass
            tags_list.append(li)
            n.send_keys(Keys.ENTER)
        # print(tags_list, len(tags_list))  # 잘 들어오고 50개 들어오는거 홛인했음
        print(tags_list)
        # json_file => 백준 : {문제번호 : ~, 제목: ~, 태그: ~}

    temp["level"] = level_
    temp["number"] = num_
    temp["title"] = title_
    temp["tags"] = tags_list
    # result[level_] = temp

    with open(
        os.path.join(BASE_DIR, "problems.json"), "w+", encoding="UTF-8"
    ) as json_file:
        json.dump(temp, json_file, ensure_ascii=False, indent=2)

    # print("끝")

    with open(
        os.path.join(BASE_DIR, "problems.json"), "r", encoding="UTF-8"
    ) as json_file:
        json_file = json.load(json_file)

    # json_file['변수명']['인덱스']로 확인 가능
    len_ = len(json_file["level"])
    print(len_)

    for ind in range(len_):
        level = json_file["level"][ind]
        number = json_file["number"][ind]
        title = json_file["title"][ind]
        tags = json_file["tags"][ind]

        if __name__ == "__main__":
            if i <= 5:
                BJData_br(level=level, number=number, title=title, tags=tags).save()
                print("브론즈 저장 완료")
            elif i <= 10:
                BJData_si(level=level, number=number, title=title, tags=tags).save()
                print("실버 저장 완료")
            elif i <= 15:
                BJData_go(level=level, number=number, title=title, tags=tags).save()
                print("골드 저장 완료")
            elif i <= 20:
                BJData_pl(level=level, number=number, title=title, tags=tags).save()
                print("플레 저장 완료")
            elif i <= 25:
                BJData_di(level=level, number=number, title=title, tags=tags).save()
                print("다이아 저장 완료")
            else:
                BJData_ru(level=level, number=number, title=title, tags=tags).save()
                print("루비 저장 완료")
driver.close()
