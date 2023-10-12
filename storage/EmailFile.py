import os
class EmailFile:
    emailReceivers = []
    def getFilePath():
        return f"data/email_receivers.txt"
    
    def readFile():
        if (os.path.isfile(EmailFile.getFilePath())):
            file = open(EmailFile.getFilePath(), "r")
            lines = file.read().splitlines()
            EmailFile.emailReceivers = list(lines)
            file.close()