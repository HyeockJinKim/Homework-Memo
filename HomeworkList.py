

class HomeworkList:
    def __init__(self):
        self.homework_list = []

    def create_homework_list(self, hw_list):
        self.make_homework_list(hw_list)
        self.homework_list_sort(self.homework_list)
        return self.homework_list

    @staticmethod
    def homework_list_sort(sort_list):
        i = 0
        homework_time = []
        for homework_data in sort_list:
            homework_time.append(int(homework_data[2][1] + homework_data[2][2]
                                     + homework_data[3][0] + homework_data[3][1]))
            i += 1
        i = 1
        while i < len(homework_time):
            j = i
            while homework_time[j] < homework_time[j - 1] and j > 0:
                homework_time[j - 1], homework_time[j] = homework_time[j], homework_time[j - 1]
                sort_list[j - 1], sort_list[j] = sort_list[j], sort_list[j - 1]
                j -= 1
            i += 1
        return sort_list

    def make_homework_list(self, hw_list):
        self.homework_list.clear()
        i = 0
        num = 1

        while i < len(hw_list):
            if num < len(hw_list[i][1]):
                hw = str(hw_list[i][1][num]).split()
                if hw[0] == '과제가':
                    i += 1
                    continue
                if hw[len(hw) - 1] == '종료':
                    num += 1
                    continue
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
                num += 1
            else:
                i += 1
                num = 1


