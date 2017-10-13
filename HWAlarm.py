import codecs
from tkinter import *
from selenium import webdriver
import datetime, time
import threading
import os
import sys
import pickle
import win32com.shell.shell as shell
ASADMIN = 'asadmin'
threads = []
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
        self.homeworkList = []
        self.homeworkFileList = []
        self.loginData = []
        self.subjectName = []
        self.homeworkName = []
        self.endTime = []
        self.remain = []
        self.login()
        autoThread = threading.Thread(target=self.autoHWloader)
        autoThread.start()
        threads.append(autoThread)


    # login 함수, login
    def login(self):
        if os.path.isfile('./loginData.bin'):
            decoder = codecs.getdecoder('hex')
            file = open('./loginData.bin', 'rb')
            idpw = bytes(decoder(file.read())[0]).decode()
            file.close()
            idpwValue = idpw.split('\n')
            self.loginData.append(idpwValue[0])
            self.loginData.append(idpwValue[1])
            self.subjectLabel = Label(self.root, text='과목')
            self.subjectLabel.grid(row=0, column=0)
            self.hwLabel = Label(self.root, text='과제 이름')
            self.hwLabel.grid(row=0, column=1)
            self.endLabel = Label(self.root, text='제출 기한')
            self.endLabel.grid(row=0, column=2)
            self.remainLabel = Label(self.root, text='남은 기간')
            self.remainLabel.grid(row=0, column=3)
            self.logoutBtn = Button(self.root, text='로그아웃', command=self.clickLogout)
            self.logoutBtn.grid(row=0, column=4)
            self.readHomeworkFileList()

        else:
            self.idInput = Label(self.root, text='아이디')
            self.idInput.grid(row=0, column=0)
            self.idValue = Entry(self.root)
            self.idValue.grid(row=0, column=1)
            self.passwordInput = Label(self.root, text='비밀번호')
            self.passwordInput.grid(row=1, column=0)
            self.passwordValue = Entry(self.root, show='*')
            self.passwordValue.grid(row=1, column=1)
            self.loginBtn = Button(self.root, text='로그인', command=self.clickLogin, height=2)
            self.loginBtn.grid(row=0, column=2, rowspan=2)

            self.root.mainloop()

    def clickLogout(self):
        if os.path.isfile('./loginData.bin'):
            os.remove('./loginData.bin')
        self.root.destroy()
        self.root = Tk()
        self.root.title("과제 시간표")
        self.subjectName.clear()
        self.homeworkName.clear()
        self.endTime.clear()
        self.remain.clear()
        self.login()

    def clickLogin(self):
        encoder = codecs.getencoder('hex')
        idpw = encoder(str(self.idValue.get() + '\n' +self.passwordValue.get()).encode())[0]
        file = open('./loginData.bin', 'wb')
        file.write(idpw)
        file.close()
        self.idInput.grid_remove()
        self.idValue.grid_remove()
        self.passwordInput.grid_remove()
        self.passwordValue.grid_remove()
        self.loginBtn.grid_remove()
        self.login()

    def refreshTime(self):
        now = datetime.datetime.now()
        nowDay = now.date()
        year = now.year
        remainDays = []
        for homeworkData in self.homeworkList:
            remainDays.append((datetime.date(int(year), int(homeworkData[2][1]), int(homeworkData[2][2]))
                               - nowDay).days)
        i = 0

        for homeworkData in self.homeworkList:
            if remainDays[i] > 1:
                homeworkData.append(str(remainDays[i]) +' 일 전..')
            else :

                remainTime = ((remainDays[i]*24+int(homeworkData[3][0]) - now.hour)) * 60 + int(homeworkData[3][1]) -now.minute
                remainTime = int((remainTime)/60)
                if remainTime > 24:
                    homeworkData.append('1 일 전..')
                elif remainTime > 0:
                    homeworkData.append(str(remainTime)+' 시간 전..')
                else :
                    homeworkData.append('1 시간 이내..')
            i += 1

    def homeworkListSort(self):
        i = 0
        hwTime = []
        for homeworkData in self.homeworkList:
            hwTime.append(int(homeworkData[2][1] + homeworkData[2][2] + homeworkData[3][0] + homeworkData[3][1]))
            i += 1
        i = 1
        while i < len(hwTime):
            j = i
            while hwTime[j] < hwTime[j-1] and j > 0:
                hwTime[j-1], hwTime[j] = hwTime[j], hwTime[j-1]
                self.homeworkList[j-1], self.homeworkList[j] = self.homeworkList[j], self.homeworkList[j-1]
                j -= 1
            i += 1

    def autoHWloader(self):
        now = datetime.time.now()
        minut = (now.minute + 5) * 60
        hour = 3600
        time.sleep(minut)
        while True:
            if self.readHomeworkList():
                i = 0
                while i < self.homeworkCount:
                    Label(self.subjectName[i]).grid_remove()
                    Label(self.homeworkName[i]).grid_remove()
                    Label(self.endTime[i]).grid_remove()
                    Label(self.remain[i]).grid_remove()
                self.subjectName.clear()
                self.homeworkName.clear()
                self.endTime.clear()
                self.remain.clear()
                self.readHomeworkFileList()
            time.sleep(hour)

    def gridHomeworkList(self):
        self.refreshTime()
        self.homeworkListSort()
        i = 0
        for homeworkData in self.homeworkList:
            timeInfo = '20' + homeworkData[2][0] + '년 ' + homeworkData[2][1]  + '월 ' + homeworkData[2][2] + '일 ' \
                       + homeworkData[3][0] + '시 ' + homeworkData[3][1] + '분까지...'
            self.subjectName.append(Label(self.root, text=homeworkData[0]))
            self.homeworkName.append(Label(self.root, text=homeworkData[1]))
            self.endTime.append(Label(self.root, text=timeInfo))
            self.remain.append(Label(self.root, text=homeworkData[4]))
            self.subjectName[i].grid(row=i + 1, column=0)
            self.homeworkName[i].grid(row=i + 1, column=1)
            self.endTime[i].grid(row=i + 1, column=2)
            self.remain[i].grid(row=i + 1, column=3)
            i += 1
        self.root.mainloop()

    def readHomeworkFileList(self):
        if not os.path.isfile('./'+self.loginData[0]+'.bin'):
            self.readHomeworkList()
        file = open('./'+self.loginData[0]+'.bin', 'rb')
        self.homeworkFileList = pickle.load(file)
        file.close()
        self.homeworkList = self.homeworkFileList
        self.gridHomeworkList()

    def equalHomeworkList(self):
        if not os.path.isfile('./' + self.loginData[0] + '.bin'):
            return False
        if self.homeworkFileList == self.homeworkList:
            return True
        else:
            return False


    def readHomeworkList(self):
        main_driver = webdriver.PhantomJS("./phantomjs.exe")
        main_driver.get("http://e-learn.cnu.ac.kr/")
        time.sleep(1)
        main_driver.find_element_by_xpath('// *[ @ id = "pop_login"]').click()
        time.sleep(1)
        main_driver.find_element_by_xpath('//*[@id="id"]').send_keys(self.loginData[0])
        main_driver.find_element_by_xpath('//*[@id="pass"]').send_keys(self.loginData[1]+'\n')
        time.sleep(5)  # 로그인 지연 시간
        main_driver.get('http://e-learn.cnu.ac.kr/lms/myLecture/doListView.dunet')
        time.sleep(1)
        self.homeworkList.clear()
        self.homeworkCount = 0
        i = 1
        try:
            while True:
                j = 1
                subjectName = main_driver.find_element_by_xpath(
                    '// *[ @ id = "rows1"] / table / tbody / tr[' + str(i) + '] / td[4] / span[1] / a').text
                subjectName = subjectName.split()[0]
                main_driver.find_element_by_xpath(
                    '// *[ @ id = "rows1"] / table / tbody / tr[' + str(i) + '] / td[4] / span[1] / a').click()

                time.sleep(1)
                main_driver.find_element_by_xpath('//*[@id="leftSnb"]/li[8]/a').click()
                time.sleep(1)
                try:
                    while True:
                        if main_driver.find_element_by_xpath('// *[ @ id = "con"] / table[2] / tbody / tr[' + str(
                                j) + '] / td[7]').text == "진행" \
                                and main_driver.find_element_by_xpath('// *[ @ id = "con"] / table[2] / tbody / tr[' + str(
                                    j) + '] / td[3]').text != '제출':
                            homeworkName = main_driver.find_element_by_xpath(
                                '// *[ @ id = "con"] / table[2] / tbody / tr[' + str(j) + '] / td[1] / strong / a').text
                            homeworkTime = main_driver.find_element_by_xpath(
                                '// *[ @ id = "con"] / table[2] / tbody / tr[' + str(j) + '] / td[2] / a').text
                            hwTime = homeworkTime.split()
                            date = hwTime[3].split('/')
                            endTime = hwTime[4].split(':')
                            self.homeworkInfo = [subjectName , homeworkName , date, endTime]
                            self.homeworkList.append(self.homeworkInfo)
                            self.homeworkCount += 1

                        j += 1
                        time.sleep(1)
                except Exception:
                    i += 1

                main_driver.get('http://e-learn.cnu.ac.kr/lms/myLecture/doListView.dunet')
        except Exception:
            if self.homeworkCount != 0:
                if not self.equalHomeworkList():
                    self.homeworkFileList = self.homeworkList
                    file = open('./'+self.loginData[0]+'.bin', 'wb')
                    pickle.dump(self.homeworkFileList, file)
                    file.close()
                    return True
                else:
                    return False

def main():
    HW = HomeworkAlarm()


if __name__ == '__main__':
    if uac_require():# 관리자 권한
        main()
    else:
        root = Tk()
        root.title("과제 시간표")
        Label(root, text='관리자 권한 받기 실패').pack()
        root.mainloop()