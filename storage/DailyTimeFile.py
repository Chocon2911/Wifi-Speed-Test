import os
class DailyTimeFile():
    dailyTime = None

    def getFilePath():
        return "data/daily_time.txt"
    def readFile():
        if os.path.isfile(DailyTimeFile.getFilePath()):
            file = open(DailyTimeFile.getFilePath(), "r")
            lines = file.read().splitlines()
            DailyTimeFile.dailyTime = lines[0]
            file.close()
        else:
            print("no daily_time.txt")