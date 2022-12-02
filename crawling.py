from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time, os, json
from selenium.webdriver.common.keys import Keys

# 데이터 저장용
import os

## Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로를 등록
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "final_pjt.settings")
## 프로젝트를 사용할 수 있도록 환경 생성
import django

django.setup()

from algorithm.models import BJData

## python파일의 위치
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# options = webdriver.ChromeOptions()
# options.add_experimental_option("excludeSwitches", ["enable-logging"])
# browser = webdriver.Chrome(options=options)

page = {
    1: 3,
    2: 4,
    3: 11,
    4: 16,
    5: 13,
    6: 13,
    7: 15,
    8: 15,
    9: 16,
    10: 15,
    11: 18,
    12: 20,
    13: 20,
    14: 18,
    15: 17,
    16: 18,
    17: 18,
    18: 19,
    19: 18,
    20: 15,
    21: 15,
    22: 14,
    23: 10,
    24: 8,
    25: 6,
    26: 5,
    27: 3,
    28: 2,
    29: 1,
    30: 1,
}
result = {}
temp = {}

for i in range(1, 31):
    driver.refresh()
    v = page[i]
    for j in range(1, int(v) + 1):
        level_ = i
        page_ = j
        print(f"{level_}레벨 {page_}페이지 시작")
        URL = f"https://solved.ac/problems/level/{level_}?page={page_}"
        driver.get(url=URL)
        # if j == 1 or j == int(v) + 1:
        driver.refresh()
        driver.implicitly_wait(1)
        time.sleep(1)

        c = driver.find_elements(By.CLASS_NAME, "css-gv0s7n")
        count = len(c)
        # level = i

        # 문제 번호
        # 한 페이지에 최대 50문제 1~50까지
        # 첫 번째 //*[@id="__next"]/div/div[4]/div[2]/div[1]/table/tbody/tr[5]/td[1]/div/div/div/span/a/span
        # 50 번째 //*[@id="__next"]/div/div[4]/div[2]/div[1]/table/tbody/tr[50]/td[1]/div/div/div/span/a/span

        num_ = []
        # url_ = []
        for k in range(1, count + 1):
            prob_num = driver.find_elements(
                By.XPATH,
                f'//*[@id="__next"]/div/div[4]/div[2]/div[1]/table/tbody/tr[{k}]/td[1]/div/div/div/span/a/span',
            )
            for number in prob_num:
                num_.append(number.text)
        # print(num_)
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
        # 마지막 //*[@id="__next"]/div/div[4]/div[2]/div[1]/table/tbody/tr[50]/td[2]/span/div/div[1]/span[1]/div/a/span
        title_ = []
        for m in range(1, count + 1):
            title = driver.find_elements(
                By.XPATH,
                f'//*[@id="__next"]/div/div[4]/div[2]/div[1]/table/tbody/tr[{m}]/td[2]/span/div/div[1]/span[1]/div/a/span',
            )
            for value in title:
                # print(value.text)
                title_.append(value.text)

        # print(len(title_))
        # print(title_)

        tags_list = []
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
                    li.append(t.text)
            else:  # 한개
                tags = driver.find_element(By.CLASS_NAME, "css-1rqtlpb")
                # print(tags.text)
                li.append(tags.text)
                # print(li)
            tags_list.append(li)
            n.send_keys(Keys.ENTER)
        # print(tags_list, len(tags_list))  # 잘 들어오고 50개 들어오는거 홛인했음

        # json_file => 백준 : {문제번호 : ~, 제목: ~, 태그: ~}

        temp["number"] = num_
        temp["title"] = title_
        temp["tags"] = tags_list
        result[level_] = temp

        with open(
            os.path.join(BASE_DIR, "problems.json"), "w+", encoding="UTF-8"
        ) as json_file:
            json.dump(result, json_file, ensure_ascii=False, indent=2)

        if __name__ == "__main__":
            bj_data_dict = result
            for le, n, ti, ta in bj_data_dict.items():
                BJData(level=le, number=n, title=ti, tags=ta).save()

        # for nu in range(count):
        #     print(num_[nu], title_[nu], tags_list[nu])


driver.close()

# while True:
#     pass
