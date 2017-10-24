import codecs
from tkinter import *
from selenium import webdriver
from functools import partial
import datetime
import time
import threading
import os
import sys
import pickle
import win32com.shell.shell as shell
ASADMIN = 'asadmin'


def uac_require():
    try:
        if sys.argv[-1] != ASADMIN:
            script = os.path.abspath(sys.argv[0])
            params = ' '.join([script] + sys.argv[1:] + [ASADMIN])
            shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)
            sys.exit(0)
        return True
    except:
        return False

"""
Kim Hyeock Jin
"""


class HomeworkAlarm:
    def __init__(self):
        self.root = Tk()
        self.root.title("과제 시간표")
        self.root.configure(background='white')
        self.timer = 0
        self.homework_list = []
        self.homework_file_list = []
        self.login_data = []
        self.subject_name = []
        self.homework_name = []
        self.end_time = []
        self.remain = []
        self.submit_btn = []
        self.submit = []
        self.timer = datetime.datetime.now().minute
        self.login()
        self.root.mainloop()

    # 로그인 로그아웃 기능
    def login(self):
        if os.path.isfile('./loginData.bin'):
            decoder = codecs.getdecoder('hex')
            file = open('./loginData.bin', 'rb')
            id_pw_value = bytes(decoder(file.read())[0]).decode()
            file.close()
            self.login_data.append(id_pw_value.split('\n')[0])
            self.login_data.append(id_pw_value.split('\n')[1])
            Label(self.root, text='과목', font='Verdana 10 bold', background='white').grid(row=0, column=0)
            Label(self.root, text='과제 이름', font='Verdana 10 bold', background='white').grid(row=0, column=1)
            Label(self.root, text='제출 기한', font='Verdana 10 bold', background='white').grid(row=0, column=2)
            Label(self.root, text='남은 기간', font='Verdana 10 bold', background='white').grid(row=0, column=3)
            Label(self.root, text='제출 여부', font='Verdana 10 bold', background='white').grid(row=0, column=4)
            Button(self.root, text='로그아웃', command=self.click_logout, background='white').grid(row=0, column=5)
            self.read_homework_file()
            self.auto = threading.Thread(target=self.auto_load_thread)
            self.auto.setDaemon(True)
            self.auto.start()

        else:
            self.id_input = Label(self.root, text='아이디', font='Verdana 10 bold')
            self.id_input.configure(background='white')
            self.id_input.grid(row=0, column=0)
            self.id_value = Entry(self.root)
            self.id_value.grid(row=0, column=1)
            self.password_input = Label(self.root, text='비밀번호', font='Verdana 10 bold')
            self.password_input.configure(background='white')
            self.password_input.grid(row=1, column=0)
            self.password_value = Entry(self.root, show='*')
            self.password_value.grid(row=1, column=1)
            self.login_btn = Button(self.root, text='로그인', command=self.click_login, height=2, font='Verdana 10 bold')
            self.login_btn.configure(background='white')
            self.login_btn.grid(row=0, column=2, rowspan=2)

    def click_login(self):
        encoder = codecs.getencoder('hex')
        id_pw_value = encoder(str(self.id_value.get() + '\n' +self.password_value.get()).encode())[0]
        file = open('./loginData.bin', 'wb')
        file.write(id_pw_value)
        file.close()
        self.id_input.destroy()
        self.id_value.destroy()
        self.password_input.destroy()
        self.password_value.destroy()
        self.login_btn.destroy()
        self.login()

    def click_logout(self):
        if os.path.isfile('./loginData.bin'):
            os.remove('./loginData.bin')
        self.root.quit()

    # 제출하기 기능
    def click_submit(self, index):
        subject_name = self.homework_list[index][0]
        homework_name = self.homework_list[index][1]
        submit_driver = webdriver.Chrome("./chromedriver.exe")
        if not self.login_homepage(submit_driver):
            return False
        time.sleep(1)
        i = 1
        try:
            while True:
                if subject_name == str(submit_driver.find_element_by_xpath('//*[@id="rows1"]/table/tbody/tr[' + str(i) + ']/td[4]/span[1]/a').text).split()[0]:
                    submit_driver.find_element_by_xpath(
                        '// *[ @ id = "rows1"] / table / tbody / tr[' + str(i) + '] / td[4] / span[1] / a').click()
                    time.sleep(1)
                    submit_driver.find_element_by_xpath('//*[@id="leftSnb"]/li[8]/a').click()
                    time.sleep(1)
                    break
                i += 1
        except Exception:
            return
        i = 1
        try:
            while True:
                if homework_name == submit_driver.find_element_by_xpath('// *[ @ id = "con"] / table[2] / tbody / tr[' + str(i) + '] / td[1] / strong / a').text:
                    submit_driver.find_element_by_xpath(
                        '// *[ @ id = "con"] / table[2] / tbody / tr[' + str(i) + '] / td[1] / strong / a').click()
                i += 1
        except Exception:
            return

    # auto thread로 계속 값을 가져옴.
    def auto_load_thread(self):
        while True:
            t = threading.Thread(target=self.auto_homework_loader)
            t.start()
            t.join()
            while self.timer < 6:
                time.sleep(600)
                self.root.after(0, self.grid_homework_list)
                self.timer += 1
            self.timer = 0

    def auto_homework_loader(self):
        self.read_homework_list()
        i = 0
        count = len(self.subject_name)
        while i < count:
            self.subject_name[i].destroy()
            self.homework_name[i].destroy()
            self.end_time[i].destroy()
            self.remain[i].destroy()
            self.submit[i].destroy()
            self.submit_btn[i].destroy()
            i += 1
        self.subject_name.clear()
        self.homework_name.clear()
        self.end_time.clear()
        self.remain.clear()
        self.submit.clear()
        self.submit_btn.clear()

        self.root.after(0, self.grid_homework_list)

    # 시간에 따라 list를 sort
    def homework_list_sort(self, sort_list):
        i = 0
        homework_time = []
        for homework_data in sort_list:
            homework_time.append(int(homework_data[2][1] + homework_data[2][2]
                                     + homework_data[3][0] + homework_data[3][1]))
            i += 1
        i = 1
        while i < len(homework_time):
            j = i
            while homework_time[j] < homework_time[j-1] and j > 0:
                homework_time[j-1], homework_time[j] = homework_time[j], homework_time[j-1]
                sort_list[j-1], sort_list[j] = sort_list[j], sort_list[j-1]
                j -= 1
            i += 1
        return sort_list

    # 남은 시간을 refresh 해줌.
    def refresh_time(self):
        now = datetime.datetime.now()
        now_day = now.date()
        year = now.year
        remain_days = []

        for homework_data in self.homework_list:
            remain_days.append((datetime.date(int(year), int(homework_data[2][1]), int(homework_data[2][2]))
                               - now_day).days)
        i = 0

        for homework_data in self.homework_list:
            if remain_days[i] > 1:
                homework_data.append(str(remain_days[i]) +' 일 전..')
            else :
                remain_time = int(((remain_days[i]*24+int(homework_data[3][0]) - now.hour) * 60
                                   + int(homework_data[3][1]) - now.minute)/60)
                if remain_time > 24:
                    homework_data.append('1 일 전..')
                elif remain_time > 0:
                    homework_data.append(str(remain_time)+' 시간 전..')
                else :
                    homework_data.append('1 시간 이내..')
            i += 1

    # ui에 적용.
    def grid_homework_list(self):
        self.refresh_time()
        i = 0
        for homework_data in self.homework_list:
            time_info = '20' + homework_data[2][0] + '년 ' + homework_data[2][1]  + '월 ' + homework_data[2][2] + '일 ' \
                       + homework_data[3][0] + '시 ' + homework_data[3][1] + '분까지...'
            self.subject_name.append(Label(self.root, text=homework_data[0], background='white'))
            self.homework_name.append(Label(self.root, text=homework_data[1], background='white'))
            self.end_time.append(Label(self.root, text=time_info, background='white'))
            self.remain.append(Label(self.root, text=homework_data[5], background='white'))
            self.submit.append(Label(self.root, text=homework_data[4], background='white'))
            action = partial(self.click_submit, i)
            self.submit_btn.append(Button(self.root, text='제출하기', command=action, background='red', foreground='white'))
            self.subject_name[i].grid(row=i + 1, column=0)
            self.homework_name[i].grid(row=i + 1, column=1)
            self.end_time[i].grid(row=i + 1, column=2)
            self.remain[i].grid(row=i + 1, column=3)
            self.submit[i].grid(row=i + 1, column=4)
            self.submit_btn[i].grid(row=i + 1, column=5)

            i += 1

    def read_homework_file(self):
        if os.path.isfile('./'+self.login_data[0]+'.bin'):
            file = open('./' + self.login_data[0] + '.bin', 'rb')
            self.homework_list = self.homework_file_list = pickle.load(file)
            file.close()
            self.grid_homework_list()

    # def equal_homework_list(self, hw_list):
    #     if not os.path.isfile('./' + self.login_data[0] + '.bin'):
    #         return False
    #     if self.homework_file_list == hw_list:
    #         return True
    #     else:
    #         return False

    def login_homepage(self, driver):
        try:
            driver.get("http://e-learn.cnu.ac.kr/")
            time.sleep(2)
            driver.find_element_by_xpath('// *[ @ id = "pop_login"]').click()
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="id"]').send_keys(self.login_data[0])
            driver.find_element_by_xpath('//*[@id="pass"]').send_keys(self.login_data[1] + '\n')
            time.sleep(1)
            driver.get('http://e-learn.cnu.ac.kr/lms/myLecture/doListView.dunet')
            time.sleep(1)
        except Exception:
            driver.quit()
            return False
        return True

    def read_homework_list(self):
        driver = webdriver.PhantomJS("./phantomjs.exe")
        if not self.login_homepage(driver):
            return False

        try:
            subject_number = len(str(driver.find_element_by_xpath('// *[ @ id = "rows1"] / table').text).split('\n'))
            subject_number = int(subject_number / 2)
            hw_list = []
            i = 0
            while i < subject_number:
                hw_list.append([])
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
                driver.switch_to_window(driver.window_handles[i])
                i += 1
                hw_list[i - 1].append(str(driver.find_element_by_xpath('//*[@id="rows1"]/table/tbody/tr[' + str(i)
                                                                       + ']/td[4]/span[1]/a').text).split()[0])
                driver.find_element_by_xpath('// *[ @ id = "rows1"] / table / tbody / tr[' + str(i)
                                             + '] / td[4] / span[1] / a').click()
                time.sleep(1)
                driver.find_element_by_xpath('//*[@id="leftSnb"]/li[8]/a').click()
                hw_list[i - 1].append(str(driver.find_element_by_xpath('// *[ @ id = "con"] / table[2] ').text).split('\n'))
            driver.quit()

            self.homework_list.clear()
            i = 0
            num = len(hw_list[i][1]) - 1
            while i < subject_number:
                hw = str(hw_list[i][1][num]).split()
                if hw[len(hw) - 1] != '종료':
                    subject_name = hw_list[i][0]
                    name_len = len(hw) - 12
                    j = 1
                    homework_name = hw[2]
                    while j < name_len:
                        homework_name += ' ' + hw[2 + j]
                        j += 1
                    date = hw[5 + name_len].split('/')
                    end_time = hw[6 + name_len].split(':')
                    submit = hw[7 + j]
                    temp = [subject_name, homework_name, date, end_time, submit]
                    self.homework_list.append(temp)
                    num -= 1
                else:
                    i += 1
                    if i < subject_number:
                        num = len(hw_list[i][1]) - 1

            self.homework_list_sort(self.homework_list)
            self.homework_file_list = self.homework_list
            file = open('./' + self.login_data[0] + '.bin', 'wb')
            pickle.dump(self.homework_list, file)
            file.close()

            return True
        except Exception:
            driver.quit()
            return False


def main():
    homework = HomeworkAlarm()


if __name__ == '__main__':
    # if uac_require():# 관리자 권한
        main()