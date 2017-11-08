from Login import Login
from selenium import webdriver
import time
import os


class Driver:
    def __init__(self):
        self.Login = Login()
        if os.name == 'posix':
            self.phantom = './phantomjs'
            self.chrome = './chromedriver'
        if os.name == 'nt':
            self.phantom = './phantomjs.exe'
            self.chrome = './chromedriver.exe'
        self.timer = 0
        self.login_count = 2
        self.homework_table = []
        self.driver_list = []

    def create_driver(self, name):
        if name == 'chrome':
            driver = webdriver.Chrome(self.chrome)
            self.driver_list.append(driver)
            return driver
        if name == 'phantom':
            driver = webdriver.PhantomJS(self.phantom)
            self.driver_list.append(driver)
            return driver

    def delete_driver(self, driver):
        try:
            driver.quit()
            self.driver_list.remove(driver)
        except Exception:
            return False
        return True

    def terminate_all_drivers(self):
        while len(self.driver_list) > 0:
            self.driver_list.pop().quit()

    def login_homepage(self, driver):
        try:
            driver.get("http://e-learn.cnu.ac.kr/")
            j = 0
            while True:
                try:
                    driver.find_element_by_xpath('// *[ @ id = "pop_login"]').click()
                    break
                except Exception:
                    j += 1
                    if j < 200:
                        time.sleep(0.1)
                    else:
                        return False

            driver.find_element_by_xpath('//*[@id="id"]').send_keys(self.Login.login_data[0])
            driver.find_element_by_xpath('//*[@id="pass"]').send_keys(self.Login.login_data[1] + '\n')
            time.sleep(self.login_count)
            driver.get('http://e-learn.cnu.ac.kr/lms/myLecture/doListView.dunet')
            j = 0
            while True:
                try:
                    subject_number = len(
                        str(driver.find_element_by_xpath('// *[ @ id = "rows1"] / table').text).split('\n'))
                    break
                except Exception:
                    j += 1
                    if j < 200:
                        time.sleep(0.1)
                    else:
                        return False

        except Exception:
            return False
        return True

    def select_subject_name(self, driver, i):
        driver.switch_to_window(driver.window_handles[i])
        j = 0
        while True:
            try:
                self.homework_table[i].append(str(driver.find_element_by_xpath('//*[@id="rows1"]/table/tbody/tr[' + str(i+1)
                                                                       + ']/td[4]/span[1]/a').text).split()[0])
                break
            except Exception:
                j += 1
                if j < 200:
                    time.sleep(0.1)
                else:
                    return False

        driver.find_element_by_xpath('// *[ @ id = "rows1"] / table / tbody / tr[' + str(i+1)
                                     + '] / td[4] / span[1] / a').click()
        return True

    @staticmethod
    def find_submit_btn(driver):
        j = 0
        while True:
            try:
                temp = str(driver.find_element_by_xpath('//*[@id="leftSnb"]').text).split('\n')
                index = 0
                while True:
                    if temp[index] == "과제제출":
                        index += 1
                        break
                    index += 1
                driver.find_element_by_xpath('//*[@id="leftSnb"]/li[' + str(index) + ']/a').click()
                break
            except Exception:
                j += 1
                if j < 200:
                    time.sleep(0.1)
                else:
                    return False
        return True

    @staticmethod
    def check_homework_name(driver, name):
        i = 1
        j = 0
        while True:
            try:
                while True:
                    if name == driver.find_element_by_xpath(
                                            '// *[ @ id = "con"] / table[2] / tbody / tr[' + str(
                                        i) + '] / td[1] / strong / a').text:
                        driver.find_element_by_xpath(
                            '// *[ @ id = "con"] / table[2] / tbody / tr[' + str(i) + '] / td[1] / strong / a').click()
                        break
                    i += 1
                break
            except Exception:
                j += 1
                if j < 200:
                    time.sleep(0.1)
                else:
                    return False
        return True

    def save_homework_table(self, driver, i):
        j = 0
        while True:
            try:
                self.homework_table[i - 1].append(
                    str(driver.find_element_by_xpath('// *[ @ id = "con"] / table[2] ').text).split('\n'))
                break
            except Exception:
                j += 1
                if j < 200:
                    time.sleep(0.1)
                else:
                    return False
        return True

    def read_homework_table(self, driver):
        try:
            subject_number = len(str(driver.find_element_by_xpath('// *[ @ id = "rows1"] / table').text).split('\n'))
            subject_number = int(subject_number / 2)
            self.homework_table.clear()
            i = 0
            while i < subject_number:
                self.homework_table.append([])
                i += 1

            i = 1
            while i < subject_number:
                driver.execute_script("window.open()")
                i += 1
            i = 1
            while i < subject_number:
                driver.switch_to_window(driver.window_handles[i])
                driver.get('http://e-learn.cnu.ac.kr/lms/myLecture/doListView.dunet')
                i += 1

            i = 0
            while i < subject_number:
                if not self.select_subject_name(driver, i):
                    return False
                i += 1

                j = 0
                if not self.find_submit_btn(driver):
                    return False

                if not self.save_homework_table(driver, i):
                    return False

        except Exception:
            return False
        return True

    def wait_terminate(self, driver):
        while len(driver.get_window_size()) == 2:
            time.sleep(5)

    # 제출하기 기능
    def submit_homework(self, driver, index):
        subject_name = self.homework_table[index][0]
        homework_name = self.homework_table[index][1]
        i = 1
        try:
            while True:
                if subject_name == str(driver.find_element_by_xpath(
                                        '//*[@id="rows1"]/table/tbody/tr[' + str(i) + ']/td[4]/span[1]/a').text).split()[0]:

                    if not self.select_subject_name(driver, i):
                        return False

                    if not self.find_submit_btn(driver):
                        return False

                    break
                i += 1
        except Exception:
            return False
        if not self.check_homework_name(driver, homework_name):
            return False
        return True
