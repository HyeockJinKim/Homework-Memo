from tkinter import *
from Driver import Driver
from HomeworkList import HomeworkList
from functools import partial
import pickle
import os
import datetime
import threading
import time


class Ui:
    def __init__(self):
        self.ui = Tk()
        self.start_ui()
        self.reader = Driver()
        self.homework = HomeworkList()
        self.timer = 0
        self.auto = threading.Thread(target=self.auto_load_thread, daemon=True)
        self.id_input = Label(self.ui, text='아이디', font='Verdana 10 bold', background='white')
        self.id_value = Entry(self.ui)
        self.password_input = Label(self.ui, text='비밀번호', font='Verdana 10 bold', background='white')
        self.password_value = Entry(self.ui, show='*')
        self.password_value.bind('<Return>', self.enter_key)
        self.login_btn = Button(self.ui, text='로그인', command=self.click_login, height=2, font='Verdana 10 bold'
                                , background='white')
        self.subject_name = []
        self.homework_name = []
        self.end_time = []
        self.remain = []
        self.submit_btn = []
        self.submit = []
        self.login()
        self.ui.mainloop()

    def start_ui(self):
        self.ui.title('과제 시간표')
        self.ui.configure(background='white')

    # Login Class
    def login(self):
        if os.path.isfile('./loginData.bin'):
            self.reader.Login.load_login_data()
            Label(self.ui, text='과목', font='Verdana 10 bold', background='white').grid(row=0, column=0)
            Label(self.ui, text='과제 이름', font='Verdana 10 bold', background='white').grid(row=0, column=1)
            Label(self.ui, text='제출 기한', font='Verdana 10 bold', background='white').grid(row=0, column=2)
            Label(self.ui, text='남은 기간', font='Verdana 10 bold', background='white').grid(row=0, column=3)
            Label(self.ui, text='제출 여부', font='Verdana 10 bold', background='white').grid(row=0, column=4)
            Button(self.ui, text='로그아웃', command=self.click_logout, background='white').grid(row=0, column=5)
            self.read_homework_file()
            self.auto.start()

        else:
            self.id_input.grid(row=0, column=0)
            self.id_value.grid(row=0, column=1)
            self.password_input.grid(row=1, column=0)
            self.password_value.grid(row=1, column=1)
            self.login_btn.grid(row=0, column=2, rowspan=2)

    def enter_key(self, event):
        self.click_login()

    def click_login(self):
        self.reader.Login.login(str(self.id_value.get()), str(self.password_value.get()))
        self.reader.Login.save_login_data()
        self.id_input.destroy()
        self.id_value.destroy()
        self.password_input.destroy()
        self.password_value.destroy()
        self.login_btn.destroy()
        self.login()

    def click_logout(self):
        if os.path.isfile('./loginData.bin'):
            os.remove('./loginData.bin')
        self.ui.quit()

    # Driver Class
    def click_submit(self, index):
        submit_driver = self.reader.create_driver('chrome')
        self.reader.login_homepage(submit_driver)
        if not self.reader.submit_homework(submit_driver, self.homework.homework_list[index]):
            self.reader.delete_driver(submit_driver)
            return
        self.reader.wait_terminate(submit_driver)
        self.reader.delete_driver(submit_driver)
        self.auto_homework_loader()

    # 남은 시간을 refresh 해줌.
    def refresh_time(self):
        now = datetime.datetime.now()
        now_day = now.date()
        year = now.year
        remain_days = []

        for homework_data in self.homework.homework_list:
            remain_days.append((datetime.date(int(year), int(homework_data[2][1]), int(homework_data[2][2]))
                                - now_day).days)
        i = 0
        remove_item =[]
        for homework_data in self.homework.homework_list:
            if remain_days[i] > 1:
                homework_data.append(str(remain_days[i]) + ' 일 전..')
            elif remain_days[i] >= 0:
                remain_time = int(((remain_days[i] * 24 + int(homework_data[3][0]) - now.hour) * 60
                                   + int(homework_data[3][1]) - now.minute) / 60)
                if remain_time > 24:
                    homework_data.append('1 일 전..')
                elif remain_time > 0:
                    homework_data.append(str(remain_time) + ' 시간 전..')
                else:
                    homework_data.append('1 시간 이내..')
            else:
                remove_item.append(homework_data)
            i += 1
        for remove in remove_item:
            self.homework.homework_list.remove(remove)

    # ui에 적용.
    def grid_homework_list(self):
        self.refresh_time()
        i = 0
        self.ui.title("과제 시간표")
        print(self.homework.homework_list)
        for homework_data in self.homework.homework_list:
            time_info = '20' + homework_data[2][0] + '년 ' + homework_data[2][1] + '월 ' + homework_data[2][2] + '일 ' \
                        + homework_data[3][0] + '시 ' + homework_data[3][1] + '분까지...'
            self.subject_name.append(Label(self.ui, text=homework_data[0], background='white'))
            self.homework_name.append(Label(self.ui, text=homework_data[1], background='white'))
            self.end_time.append(Label(self.ui, text=time_info, background='white'))
            self.remain.append(Label(self.ui, text=homework_data[5], background='white'))
            self.submit.append(Label(self.ui, text=homework_data[4], background='white'))
            self.submit_btn.append(Button(self.ui, text='제출하기',
                                          command=threading.Thread(target=partial(self.click_submit, i),
                                                                   daemon=True).start, background='red',
                                          foreground='white'))
            self.subject_name[i].grid(row=i + 1, column=0)
            self.homework_name[i].grid(row=i + 1, column=1)
            self.end_time[i].grid(row=i + 1, column=2)
            self.remain[i].grid(row=i + 1, column=3)
            self.submit[i].grid(row=i + 1, column=4)
            self.submit_btn[i].grid(row=i + 1, column=5)
            i += 1

    def read_homework_file(self):
        if os.path.isfile('./' + self.reader.Login.login_data[0] + '.bin'):
            file = open('./' + self.reader.Login.login_data[0] + '.bin', 'rb')
            self.homework.homework_list = pickle.load(file)
            file.close()
            self.grid_homework_list()

    def save_homework_file(self):
        file = open('./' + self.reader.Login.login_data[0] + '.bin', 'wb')
        pickle.dump(self.homework.homework_list, file)
        file.close()

    # auto thread 로 계속 값을 가져옴.
    def auto_load_thread(self):
        while True:
            self.auto_homework_loader()
            time.sleep(30 - (datetime.datetime.now().minute % 30))
            while self.timer < 4:
                time.sleep(1800)
                self.ui.after(0, self.grid_homework_list)
                self.timer += 1
            self.timer = 0

    def auto_homework_loader(self):
        auto_driver = self.reader.create_driver('phantom')
        self.ui.title('과제 시간표   (로그인...)')
        if not self.reader.login_homepage(auto_driver):
            self.ui.title('과제 시간표   로그인 실패')
            self.reader.delete_driver(auto_driver)
            return
        self.ui.title('과제 시간표   (읽는 중...)')
        if not self.reader.read_homework_table(auto_driver):
            self.ui.title('과제 시간표   읽기 실패')
            self.reader.delete_driver(auto_driver)
            return
        self.reader.delete_driver(auto_driver)
        self.homework.create_homework_list(self.reader.homework_table)
        self.save_homework_file()
        self.refresh_ui()

    def refresh_ui(self):
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
        self.ui.after(0, self.grid_homework_list)