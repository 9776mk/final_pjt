from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import subprocess
import shutil
from collections import defaultdict
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

try:
    shutil.rmtree(r"c:\chrometemp")  # 쿠키 / 캐쉬파일 삭제
except FileNotFoundError:
    pass

subprocess.Popen(
    r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"'
)  # 디버거 크롬 구동


option = Options()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

chrome_ver = chromedriver_autoinstaller.get_chrome_version().split(".")[0]


try:
    driver = webdriver.Chrome(f"./{chrome_ver}/chromedriver.exe", options=option)
except:
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(f"./{chrome_ver}/chromedriver.exe", options=option)

# 백준 레벨 : 1~30
# 페이지 최대 : 20
for i in range(1, 30):
    for j in range(1, 20):
        i = i
        j = j

        URL = f"https://solved.ac/problems/level/{i}?page={j}"
        driver.get(url=URL)
        driver.refresh()
        driver.implicitly_wait(5)
        time.sleep(5)
        # 경로로 찾아줌
        # search_box = driver.find_element_by_xpath('')
        level = i

        prob_num = driver.find_elements(
            By.XPATH,
            '//*[@id="__next"]/div/div[4]/div[2]/div[1]/table/tbody/tr[1]/td[1]/div/div/div/span/a/span',
        )
        title = driver.find_elements(By.CLASS_NAME, "__Latex__")
        category = driver.find_elements(By.CLASS_NAME, "css-18la3yb")

        print(level, prob_num, title, category)

while True:
    pass
