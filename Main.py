from tkinter import *
from selenium import webdriver
import time

def main():
    # main_driver = webdriver.Chrome("chromedriver.exe")
    main_driver = webdriver.PhantomJS("phantomjs.exe")
    root = Tk()
    root.title("과제 시간표")

    main_driver.get("http://e-learn.cnu.ac.kr/")

    main_driver.find_element_by_xpath('// *[ @ id = "pop_login"]').click()
    main_driver.find_element_by_xpath('//*[@id="id"]').send_keys('201502043')
    main_driver.find_element_by_xpath('//*[@id="pass"]').send_keys('19961228\n')
    time.sleep(5) # 로그인 지연 시간

    # userName = main_driver.find_element_by_xpath('// *[ @ id = "header_top"] / p / span / strong').text
    # user = Label(root, text=userName)
    # user.pack()
    main_driver.get('http://e-learn.cnu.ac.kr/lms/myLecture/doListView.dunet')

    i = 1
    try :
        while True :
            j = 1
            subjectName = main_driver.find_element_by_xpath('// *[ @ id = "rows1"] / table / tbody / tr[' + str(i) + '] / td[4] / span[1] / a').text
            # subject = Label(root, text=subjectName)
            # subject.pack()
            subjectName = subjectName.split()[0]
            main_driver.find_element_by_xpath('// *[ @ id = "rows1"] / table / tbody / tr[' + str(i) + '] / td[4] / span[1] / a').click()
            i += 1
            time.sleep(1)
            main_driver.find_element_by_xpath('//*[@id="leftSnb"]/li[8]/a').click()
            time.sleep(1)
            try:
                while True :

                    if main_driver.find_element_by_xpath('// *[ @ id = "con"] / table[2] / tbody / tr['+ str(j) +'] / td[7]').text == "진행" :
                        homeworkName = main_driver.find_element_by_xpath('// *[ @ id = "con"] / table[2] / tbody / tr['+ str(j) +'] / td[1] / strong / a').text
                        homeworkTime = main_driver.find_element_by_xpath('// *[ @ id = "con"] / table[2] / tbody / tr['+ str(j) +'] / td[2] / a').text
                        hwTime = homeworkTime.split()
                        homeworkInfo = subjectName + ' ' + homeworkName + ' ::' + hwTime[3] + ' '+hwTime[4]
                        homwork = Label(root, text= homeworkInfo)
                        homwork.pack()
                    j += 1
                    time.sleep(1)
            except Exception :
                print()

            main_driver.get('http://e-learn.cnu.ac.kr/lms/myLecture/doListView.dunet')
    except Exception :
        root.mainloop()





if __name__ == '__main__':
    main()
