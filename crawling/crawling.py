from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# driver.get("https://solved.ac/problems/level/1?page=1")
# driver.refresh()

# options = webdriver.ChromeOptions()
# options.add_experimental_option("excludeSwitches", ["enable-logging"])
# browser = webdriver.Chrome(options=options)

for i in range(1, 30):
    driver.refresh()

    for j in range(1, 20):
        URL = f"https://solved.ac/problems/level/{i}?page={j}"
        driver.get(url=URL)

        if j == 1 or j == 20:
            driver.refresh()

        driver.implicitly_wait(3)
        time.sleep(3)

        level = i

        # 번호 뽑히는 것 확인
        # 한 페이지에 최대 50문제 1~50까지
        # 첫 번째 //*[@id="__next"]/div/div[4]/div[2]/div[1]/table/tbody/tr[5]/td[1]/div/div/div/span/a/span
        #  50 번째 //*[@id="__next"]/div/div[4]/div[2]/div[1]/table/tbody/tr[50]/td[1]/div/div/div/span/a/span
        # for k in range(1, 50):
        #    prob_num = driver.find_elements(
        #        By.XPATH,
        #        f'//*[@id="__next"]/div/div[4]/div[2]/div[1]/table/tbody/tr[{k}]/td[1]/div/div/div/span/a/span',
        #    )
        #    for i in prob_num:
        #        print(i.text)

        # print(f"prob_num : {prob_num}")

        # title 뽑히는 것 확인
        # title = driver.find_elements(By.CLASS_NAME, "__Latex__")
        # for value in title:
        #    print(value.text)

        for_category = driver.find_elements(By.CLASS_NAME, "css-p7gtta")
        for i in for_category:
            # i.click() element not interactable 에러 발생
            i.send_keys(Keys.ENTER)

        category = driver.find_elements(By.CLASS_NAME, "css-18la3yb")
        for i in category:
            print(i.text)

        print(f"level : {level}")
        # print(f"prob_num : {prob_num}")
        # print(title)
        # print(category)


driver.close()

while True:
    pass
