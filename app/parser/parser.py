import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager


def get_timetable():
    answer = dict()
    answer["message"] = "ok"

    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Remote(
            command_executor="http://45.151.155.164:4444/wd/hub",
            options=chrome_options,
        )

        driver.get("https://takvim.tj/")
        today_timetable = driver.find_element(
            By.CSS_SELECTOR, "#wb_element_instance27 #table_namoz_time_today"
        )

        list_times = today_timetable.find_elements(
            By.CSS_SELECTOR, "tr:has(.td_namoz_time_today)"
        )

        times = dict()

        for namoz_time in list_times:
            title = namoz_time.find_element(By.CSS_SELECTOR, ".th_namoz_time_today")
            data = namoz_time.find_element(By.CSS_SELECTOR, ".td_namoz_time_today")

            times[title.text.lower()] = data.text

        answer["times"] = times

        driver.quit()
    except Exception as exception:
        answer["message"] = str(exception)

    return answer


def write_to_file(path: str, json: str):
    with open(path, "w") as file:
        file.write(json)


def write_timetable_to_json(path="./app/parser/data.json"):
    print("Hello")
    timetable = get_timetable()
    print(timetable)
    timetable_json = json.dumps(timetable, ensure_ascii=False)
    write_to_file(path, timetable_json)


if __name__ == "__main__":
    # print("Writing...")
    # write_timetable_to_json("")
    # print("Done!")
    ...
