import os
class SlowSpeedFile():
    slowSpeed = 5
    slowSpeedLimit = 6
    slowSpeedList = [None]
    def getFilePath():
        return f"data/slow_speed.txt"
    def readFile():
        if os.path.isfile(SlowSpeedFile.getFilePath()):
            file = open(SlowSpeedFile.getFilePath(), "r")
            lines = file.read().splitlines()
            SlowSpeedFile.slowSpeed = int(lines[0])
            SlowSpeedFile.slowSpeedLimit = int(lines[1])
            print(f"{SlowSpeedFile.slowSpeed}")
            print(f"{SlowSpeedFile.slowSpeedLimit}")
            file.close()
        else:
            print("no slow_speed.txt")