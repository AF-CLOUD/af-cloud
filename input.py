import datetime

class CInput:

    def __init__(self):
        self.__keyword = None
        self.__m_period = list()
        self.__c_period = None
        self.__is_trashed = None

    def set_gdrive_inputs(self):
        """
            # 입력이 형식에 맞게 제대로 이루어졌는지 확인하는 코드 추가 필요함 #
        :return:
        """
        # 1. keyword
        self.__set_keyword()
        # 2. modified
        self.__set_m_period()

    def __set_keyword(self):
        print("\n"
              "Setting Keywords to search in file name\n"
              "If you don't want to set keyword, please click enter\n")
        self.__keyword = input("Input your Keyword: ")

    def __set_m_period(self):
        print("\n"
              "Setting Files modified after a given date\n"
              "If you don't want to set period, please click enter\n"
              "period input example: 2021-06-04\n")
        start_time = input("Input the Start Time Point: ")
        end_time = input("Input the End Time Point: ")

        if start_time == '':
            start_time = "1970-01-01"
        if end_time == '':
            end_time = datetime.datetime.now().strftime("%Y-%m-%d")
        self.__m_period.append(start_time)
        self.__m_period.append(end_time)

    def get_keyword(self):
        return self.__keyword

    def get_m_period(self):
        return self.__m_period

    def show_input(self):
        print("\n"
              "======SHOW_INPUT======")
        print("Keyword : ", self.__keyword)
        print("mPeriod : ", self.__m_period)
