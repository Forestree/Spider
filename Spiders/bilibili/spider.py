from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException


# 等待页面加载10条以上
class WaitForHistoryTitle(object):
    def __init__(self, loaded_num):
        self.loaded_num = loaded_num

    def __call__(self, driver):
        if len(driver.find_elements_by_css_selector('.title')) - self.loaded_num >= 10:
            return True
        return False


class Bilibili(object):
    MAX_PAUSE_TIME = 5
    login_url = 'https://passport.bilibili.com/login'

    def __init__(self, cookies, driver=None):
        if not driver:
            option = ChromeOptions()
            option.add_experimental_option('excludeSwitches', ['enable-automation'])
            self.driver = webdriver.Chrome(options=option)
        else:
            self.driver = driver
        for cookie_dict in cookies:
            self.driver.add_cookie(cookie_dict)

    # 获取B站观看历史
    def get_user_history(self, max_history_record=0xfffff):
        history_url = 'https://www.bilibili.com/account/history'
        self.driver.get(history_url)

        last_height = self.driver.execute_script("return document.body.scrollHeight")

        loaded_title_num = 0
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                WebDriverWait(self.driver, Bilibili.MAX_PAUSE_TIME).until(WaitForHistoryTitle(loaded_title_num))
                loaded_title_num = len(self.driver.find_elements_by_css_selector('.title'))
            except Exception as exception:
                pass
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height or loaded_title_num >= max_history_record:
                break
            last_height = new_height
        return [title.text for title in self.driver.find_elements_by_css_selector('.title')]

    # 获取B站关注的UP主
    def get_following_user(self):
        space_url = 'https://space.bilibili.com'
        self.driver.get(space_url)
        self.driver.find_element_by_css_selector('.n-statistics a').click()
        following_users = []
        WebDriverWait(self.driver, Bilibili.MAX_PAUSE_TIME).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span.be-pager-total'))
        )
        total_page_span = self.driver.find_element_by_css_selector('span.be-pager-total')
        print(total_page_span.text)
        total_page_number = int(total_page_span.text[2])
        page = 1
        while True:
            WebDriverWait(self.driver, Bilibili.MAX_PAUSE_TIME).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.list-item.clearfix .content a span'))
            )
            stale_element = True
            while stale_element:
                try:
                    text_list = [user.text for user in self.driver.find_elements_by_css_selector('.list-item.clearfix .content a span')]
                    if len(text_list) == len([text for text in text_list if text]):
                        following_users.extend(text_list)
                        stale_element = False
                except:
                    pass
            if page == total_page_number:
                break
            next_button = self.driver.find_element_by_css_selector('.be-pager-next a')
            next_button.click()
            page += 1

        return following_users





