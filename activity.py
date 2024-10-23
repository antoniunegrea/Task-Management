class Activity:
    def __init__(self, name, duration, prerequisites):
        self.__name = name
        self.__duration = duration
        self.__prerequisites = prerequisites
        self.__early = 0
        self.__late = 0

    def __str__(self):
        prerequisites_str = ""
        for p in self.__prerequisites:
            prerequisites_str += p + "; "
        if len(prerequisites_str) == 0:
            prerequisites_str = "None;"
        return f"activity: {self.__name}, duration: {self.__duration}, prerequisites: {prerequisites_str}"

    def getName(self):
        return self.__name

    def getDuration(self):
        return self.__duration

    def getPrerequisites(self):
        return self.__prerequisites

    def getEarly(self):
        return self.__early

    def getLate(self):
        return self.__late

    def setEarly(self, x):
        self.__early = x

    def setLate(self, x):
        self.__late = x
