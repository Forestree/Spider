from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import requests
from lxml import etree

class WaitForLoadTitle(object):
    def __init__(self, loaded_num):
        self.loaded_num = loaded_num

    def __call__(self, driver):
        if len(driver.find_elements_by_css_selector('.List-item h2 a')) - self.loaded_num >= 5:
            return True
        return False

class Zhihu(object):
    login_url = 'https://www.zhihu.com/signin'
    SCROLL_PAUSE_TIME = 5

    def __init__(self, cookies, driver=None):
        if not driver:
            option = ChromeOptions()
            option.add_experimental_option('excludeSwitches', ['enable-automation'])
            self.driver = webdriver.Chrome(options=option)
        else:
            self.driver = driver
        for cookie_dict in cookies:
            self.driver.add_cookie(cookie_dict)
        self.wait = WebDriverWait(self.driver, 20)
        self.personal_url = ''

    def scroll_to_bottom(self):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def get_personal_url(self):
        if self.personal_url == '':
            self.driver.get('https://www.zhihu.com/follow')
            self.driver.find_element_by_css_selector('.AppHeader-profile .Popover.AppHeader-menu button').click()
            self.driver.find_element_by_css_selector('a.Button.Menu-item').click()
            self.personal_url = self.driver.current_url
        return self.personal_url

    # 获取知乎关注的问题
    def get_following_questions(self):
        self.driver.get(self.get_personal_url() + '/following/questions')
        page = 1
        title_list = []
        while True:
            self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.List-item a')))

            titles_one_page = []

            stale_element = True
            while stale_element:
                try:
                    titles_one_page = [title.text for title in self.driver.find_elements_by_class_name('List-item a')]
                    stale_element = False
                except:
                    pass

            title_list.extend(titles_one_page)

            next_button = None
            try:
                next_button = self.driver.find_element_by_css_selector('button.Button.PaginationButton.PaginationButton-next.Button--plain')
            except:
                break
            next_button.click()

            page += 1
        return title_list

    # 获取知乎关注的主题
    def get_following_topics(self):
        self.driver.get(self.get_personal_url() + '/following/topics')
        page = 1
        title_list = []
        while True:
            self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.List-item a')))

            titles_one_page = []

            titles_one_page = [title.text for title in self.driver.find_elements_by_class_name('List-item a.TopicLink')]

            title_list.extend(titles_one_page)

            try:
                next_button = self.driver.find_element_by_css_selector('button.Button.PaginationButton.PaginationButton-next.Button--plain')
            except:
                break
            next_button.click()

            page += 1
        return title_list

    # 获取知乎推荐的有关问题
    def get_related_questions(self, max_questions_num=0xffffff):
        self.driver.get(self.get_personal_url())

        loaded_questions_num = 0
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                WebDriverWait(self.driver, Zhihu.SCROLL_PAUSE_TIME).until(WaitForLoadTitle(loaded_questions_num))
            except:
                break
            loaded_questions_num = len(self.driver.find_elements_by_css_selector('.List-item h2 a'))
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height or loaded_questions_num >= max_questions_num:
                break
            last_height = new_height
        return [question.text for question in self.driver.find_elements_by_css_selector('.List-item h2 a')]

