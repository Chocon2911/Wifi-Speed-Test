import os
class TimeLoopFile:
    normalRunLoop = 100
    slowRunLoop = 100
    restingRunLoop = 100
    def getFilePath():
        return f"data/loop_time.txt"
    
    def readFile():
        if os.path.isfile(TimeLoopFile.getFilePath()):
            file = open(TimeLoopFile.getFilePath(), "r")
            lines = file.read().splitlines()
            TimeLoopFile.normalRunLoop = int(lines[0])
            TimeLoopFile.slowRunLoop = int(lines[1])
            TimeLoopFile.restingRunLoop = int(lines[2])
            print(f"{TimeLoopFile.normalRunLoop}")
            print(f"{TimeLoopFile.slowRunLoop}")
            print(f"{TimeLoopFile.restingRunLoop}")
            file.close()
        else:
            print("no loop_time.txt")