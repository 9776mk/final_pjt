from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get("https://solved.ac/problems/level/1?page=1")
driver.refresh()

# options = webdriver.ChromeOptions()
# options.add_experimental_option("excludeSwitches", ["enable-logging"])
# browser = webdriver.Chrome(options=options)

for i in range(1, 30):
    for j in range(1, 20):
        i = i
        j = j

        URL = f"https://solved.ac/problems/level/{i}?page={j}"
        driver.get(url=URL)
        driver.refresh()
        driver.implicitly_wait(5)
        time.sleep(5)

        level = i
        prob_num = driver.find_elements(
            By.XPATH,
            '//*[@id="__next"]/div/div[4]/div[2]/div[1]/table/tbody/tr[1]/td[1]/div/div/div/span/a/span',
        )
        title = driver.find_elements(By.CLASS_NAME, "__Latex__")
        category = driver.find_elements(By.CLASS_NAME, "css-18la3yb")

        print(level)
        print(prob_num)
        print(title)
        print(category)


driver.close()

while True:
    pass
