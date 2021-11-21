import time


class RateCounter(object):
    def __init__(self, name, log_count):
        self.name = name
        self.__counter = 0
        self.__log_count = log_count
        self.__start_time = None
        self.__end_time = None

    def start(self):
        self.__counter = 0
        self.__start_time = time.time()

    def add_to_count(self):
        self.__counter += 1
        if self.__counter == self.__log_count:
            self.__end_time = time.time()
            print(self.name + ": " + str(self.__counter / (self.__end_time - self.__start_time)) + " fps")
            self.__counter = 0
            self.__start_time = time.time()

