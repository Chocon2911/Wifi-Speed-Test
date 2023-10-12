
import speedtest
import schedule
import time

from datetime import datetime

from storage.EmailFile import EmailFile
from storage.TimeLoopFile import TimeLoopFile
from storage.SlowSpeedFile import SlowSpeedFile
from storage.Mail import Mail
from storage.Other import Other
from storage.Sheet import Sheet
from storage.DailyTimeFile import DailyTimeFile
from storage.DataBase import DataBase

runLoop = 1

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "19zWNRUC1pLfVSpV5IEHP1tcV_Ptvu0F032xad4iG_WE"

class Run:
    def ScheduleTime():
        DailyTimeFile.readFile()
        schedule.every(runLoop).seconds.do(Run.MeasureSpeed)
        schedule.every().day.at(str(DailyTimeFile.dailyTime)).do(Sheet.RunSheet)
        schedule.every().day.at(str(DailyTimeFile.dailyTime)).do(Mail.SendMail)

    def MeasureSpeed():
        global runLoop
        if(Other.IsInternetAvailable()):
            EmailFile.readFile()
            wifi = speedtest.Speedtest(secure=True)
            downloadSpeed = Other.BitsToMb(wifi.download())
            downloadTime_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            downloadTime_time = Other.convertStrToTime(downloadTime_str)
            DataBase.loadDb(downloadTime_time, downloadSpeed)

            print(downloadTime_time, " Download:", downloadSpeed)

            # SpeedFile.checkFile(downloadSpeed, downloadTime_time)
            Run.CheckSpeed(downloadSpeed)
        else:
            downloadSpeed = 0
            downloadTime_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            downloadTime_time = Other.convertStrToTime(downloadTime_str)
            DataBase.loadDb(downloadTime_time, downloadSpeed)

            print("no internet")
            Mail.SendMail()
            runLoop = 170
            
    def CheckSpeed(downloadSpeed):
        global runLoop
        SlowSpeedFile.readFile()
        TimeLoopFile.readFile()
        if(downloadSpeed < SlowSpeedFile.slowSpeed):
            SlowSpeedFile.slowSpeedList.append(downloadSpeed)
            runLoop = TimeLoopFile.slowRunLoop
        if(downloadSpeed >= SlowSpeedFile.slowSpeed):
            SlowSpeedFile.slowSpeedList.clear()
            runLoop = TimeLoopFile.normalRunLoop
        if(len(SlowSpeedFile.slowSpeedList) >= SlowSpeedFile.slowSpeedLimit):
            Mail.SendMail()
            runLoop = TimeLoopFile.restingRunLoop
        schedule.clear()
        Run.ScheduleTime()

def Main():
    global runLoop
    Run.ScheduleTime()

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    Main()
    