import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
sys.path.append("../../Spiders/")


class SpiderHelper:
    def __init__(self):
        return

    def Automation(self, url):
        option = ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.driver = webdriver.Chrome(options=option)
        url = str(url)
        self.driver.get(url)
        print('After Automation')

    def getCookie3(self, login_url, quit):
        self.Automation(login_url)
        cookie_str = ''
        while 1:
            time.sleep(0.2)
            if self.driver.current_url != login_url:
                get_cookies = self.driver.get_cookies()
                cookie_str = ''
                for s in get_cookies:
                    cookie_str = cookie_str + s['name'] + '=' + s['value'] + ';'
                if quit == 1:
                    self.driver.quit()
                break
        return cookie_str

    def getCookie2(self, login_url, curr_url, extra_url, quit):
        self.Automation(login_url)
        cookie_str = ''
        while 1:
            time.sleep(0.2)
            if self.driver.current_url == curr_url:
                if extra_url == '':
                    self.driver.get(extra_url)
                get_cookies = self.driver.get_cookies()
                cookie_str = ''
                for s in get_cookies:
                    cookie_str = cookie_str + s['name'] + '=' + s['value'] + ';'
                if quit == 1:
                    self.driver.quit()
                break
        return cookie_str

    def getCookie(self, login):
        while True:
            try:
                if self.driver.get_log('driver')[0]['level'] == "WARNING":
                    return 0
            except:
                pass

            time.sleep(1)

            try:
                # if not login -> exception
                self.driver.find_element_by_css_selector(login)
            except Exception as e:
                #print(e)
                pass
            else:
                cookie_list = self.driver.get_cookies()
                self.driver.close()

                res = ''
                for cookie in cookie_list:
                    res += cookie.get('name') + '=' + cookie.get('value').replace('\"', '') + ';'
                return res

class LoginHelper(object):
    def __init__(self, driver=None):
        if not driver:
            option = ChromeOptions()
            option.add_experimental_option('excludeSwitches', ['enable-automation'])
            self.driver = webdriver.Chrome(options=option)
        else:
            self.driver = driver
        self.cookies = None

    def login(self, login_url):
        self.driver.get(login_url)
        WebDriverWait(self.driver, 100).until(EC.url_changes(login_url))
        self.cookies = self.driver.get_cookies()

    def get_driver(self):
        return self.driver

    def get_cookies(self):
        return self.cookies

    def quit_driver(self):
        self.driver.quit()

    def get_cookie_str(self):
        cookie_list = self.driver.get_cookies()

        cookie_str = ''
        for s in cookie_list:
            cookie_str = cookie_str + s['name'] + '=' + s['value'] + ';'
        return cookie_str
