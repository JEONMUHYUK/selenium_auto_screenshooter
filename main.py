import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.remote.command import Command


class GoogleKeywordScreenshooter:
    def __init__(self, keyword, screenshots_dir, max_page):
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        self.keyword = keyword
        self.screenshots_dir = screenshots_dir
        self.max_page = max_page

    def start(self):
        self.browser.get("https://google.com")
        search_bar = self.browser.find_element_by_class_name(
            "gLFyf"
        )  # classname을 찾아주는 것
        search_bar.send_keys(self.keyword)  # key값을 보내주는 메소드.
        search_bar.send_keys(Keys.ENTER)  # key값이 enter 즉 엔터를 눌러주는 메소드

        for n in range(1, self.max_page):
            try:
                shitty_element = WebDriverWait(self.browser, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "g-blk"))
                )
                self.browser.execute_script(
                    """
                const shitty = arguments[0]
                shitty.parentElement.removeChild(shitty)
                """,
                    shitty_element,
                )  # 파이썬으로 메소드 brower.execute_script()를 통해 자바스크립트를 동작,
                # 또 한 인자를 보낼 수 있다.
            except Exception:
                pass
            search_results = self.browser.find_elements_by_class_name("g")
            for index, search_result in enumerate(search_results):
                front_num = n - 1
                search_result.screenshot(
                    f"{self.screenshots_dir}/{self.keyword}x{front_num}{index}.png"
                )

            next_page_bar = self.browser.find_elements_by_id("pnnext")

            if next_page_bar:
                try:
                    next_page_bar[0].click()
                except:
                    break

    def finish(self):
        self.browser.quit()


domain_competitors = GoogleKeywordScreenshooter("buy domain", "screenshots", 5)
domain_competitors.start()
domain_competitors.finish()
