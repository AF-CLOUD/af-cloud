import datetime

class CInput:

    def __init__(self):
        self.__keyword_name = None
        self.__keyword_text = None
        self.__m_period = list()
        self.__c_period = None
        self.__is_trashed = None

    def set_gdrive_inputs(self):
        """
            # 입력이 형식에 맞게 제대로 이루어졌는지 확인하는 코드 추가 필요함 #
        :return:
        """
        # 1. keyword
        self.__set_keyword_name()
        self.__set_keyword_text()
        # 2. modified
        self.__set_m_period()

    def __set_keyword_name(self):
        print("\n"
              "Set keyword to search in name.\n"
              "If you don't want to set keyword, hit enter.\n"
              "Example input: police")
        self.__keyword_name = input("Put keyword: ")

    def __set_keyword_text(self):
        print("\n"
              "Set keyword to search in full text.\n"
              "If you don't want to set keyword, hit enter.\n"
              "Example input: lab")
        self.__keyword_text = input("Put keyword: ")

    def __set_m_period(self):
        print("\n"
              "Set period to search modified time.\n"
              "If you don't want to set period, hit enter.\n"
              "Example input: 2021-06-04\n")
        start_time = input("Put start time: ")
        end_time = input("Put end time: ")

        if start_time == '':
            start_time = "1970-01-01"
        if end_time == '':
            end_time = datetime.datetime.now().strftime("%Y-%m-%d")
        self.__m_period.append(start_time)
        self.__m_period.append(end_time)

    def get_keyword_name(self):
        return self.__keyword_name

    def get_keyword_text(self):
        return self.__keyword_text

    def get_m_period(self):
        return self.__m_period

    def show_input(self):
        print("\n"
              "======SHOW_INPUT======")
        print("Keyword-name : ", self.__keyword_name)
        print("Keyword-text : ", self.__keyword_text)
        print("Period-modified : ", self.__m_period)
