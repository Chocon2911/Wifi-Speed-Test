import os
import speedtest
import schedule
import time
import requests
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders

from datetime import datetime
from storage.SpeedNetwork import SpeedNetwork
from email.mime.base import MIMEBase

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

sheetName = None

emailSender = "speed-test@liva.com.vn"
passwordSender = "#&u){13e7$m_"
emailReceiverList = ["lavietdung@gmail.com",
    "huylexuan2911@gmail.com"]

serverMail = "mail.liva.com.vn"
port = 2525

downloadSpeed = None
downloadHour = None

speedList = []

slowSpeedList = []

runLoop = 1

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

SPREADSHEET_ID = "19zWNRUC1pLfVSpV5IEHP1tcV_Ptvu0F032xad4iG_WE"

def BitsToMb(sizeBits):
    size = round(sizeBits / (1024 * 1024), 2)
    return size

def IsInternetAvailable():
    try:
        requests.get("http://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

def ScheduleTime():
    schedule.every(runLoop).seconds.do(Run)
    schedule.every().day.at('23:50').do(RunSheet)


def SendMail():
    global SendMail
    global passwordSender
    global serverMail
    global emailReceiverList
    for i in range(len(emailReceiverList)):
        if IsInternetAvailable():
            subject = f"Wifi Speed Test {GetSheetName()}"
            message = "This is auto mail"

            msg = MIMEMultipart()
            msg["From"] = emailSender
            msg["To"] = emailReceiverList[i]
            msg["Subject"] = subject
            msg.attach(MIMEText(message, "plain"))

            filePath = f"{GetSheetName()}.txt"

            attachment = open(f"data\{filePath}", 'rb')
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= " + filePath)
            msg.attach(part)
            attachment.close()

            try:
                print("connecting to sever...")
                server = smtplib.SMTP(serverMail, port)
                server.starttls()
                server.login(emailSender, passwordSender)
                print("connected to sever")
                server.sendmail(emailSender, emailReceiverList[i], msg.as_string())
                print("sent mail")
                server.quit()
            except Exception as e:
                print("error sending", str(e))


def GetFilePath():
    fileDate = datetime.now().strftime("%Y-%m-%d")
    return f"data\{fileDate}.txt"

def ReadFile():
    global speedList
    speedList.clear()
    if (os.path.isfile(GetFilePath())):
        file = open(GetFilePath(), "r")
        for line in file:
            lineArray = line.split()
            time = lineArray[0]
            speed = lineArray[1]
            speedList.append(SpeedNetwork(time, speed))
        if(len(speedList) > 0):
            for i in range(len(speedList)):
                print(speedList[i].time)
                print(speedList[i].speed)
        else:
            speedList.clear()
        file.close()

def CreateFile():
    file = open(GetFilePath(), "x")
    file.close()

def CheckFile(speed, time):
    if (os.path.isfile(GetFilePath()) == False):
        CreateFile()
    writeFile(speed, time)
        
def writeFile(speed, time):
        f = open(GetFilePath(), "a")
        f.write(f"{time} {str(speed)}\n")
        f.close()

def Run():
    global downloadSpeed
    global downloadHour
    wifi = speedtest.Speedtest()
    downloadSpeed = BitsToMb(wifi.download())
    downloadHour = datetime.now().strftime("%H:%M:%S")

    print(downloadHour, " Download:", downloadSpeed)
    CheckFile(downloadSpeed, downloadHour)
    CheckSpeed()

def CheckSpeed():
    global runLoop
    global slowSpeedList
    slowSpeed = 5
    slowLimit = 6
    if(downloadSpeed < slowSpeed):
        slowSpeedList.append(downloadSpeed)
        runLoop = 2
    if(downloadSpeed >= slowSpeed):
        slowSpeedList.clear()
        runLoop = 50
    if(len(slowSpeedList) >= slowLimit):
        SendMail()
        runLoop = 170
    schedule.clear()
    ScheduleTime()

def GetSheetName():
    today = datetime.now().strftime("%Y-%m-%d")
    return f"{today}"

def RunSheet():
    global SPREADSHEET_ID
    if IsInternetAvailable():
        try:
            credentials = None
            if os.path.exists("token.json"):
                credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
            if not credentials or not credentials.valid:
                if credentials and credentials.expired and credentials.refresh_token:
                    credentials.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
                    credentials = flow.run_local_server(port=0)
                with open("token.json", "w") as token:
                    token.write(credentials.to_json())
            CreateSheet(credentials)
        except HttpError as error:
            print(error)
    else:
        print("no internet")
        time.sleep(60)
        RunSheet()

def CreateSheet(credentials):
        global SPREADSHEET_ID
        service = build("sheets", "v4", credentials=credentials)
        # create google sheet file
        spreadsheet_body = {
            "properties": {
                "title": GetSheetName()
            }
        }

        sheets = service.spreadsheets().create(body=spreadsheet_body)
        response = sheets.execute()
        SPREADSHEET_ID = response["spreadsheetId"]

        # create work sheet for google sheet file
        worksheet_body = {
            "requests": [
                {
                    "addSheet": {
                        "properties": {
                            "title": "Wifi_Speed_Test"
                        }
                    }
                }
            ]
        }
        service.spreadsheets().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body=worksheet_body
        ).execute()
        pushToSheet(service)

def pushToSheet(service):
    global SPREADSHEET_ID
    ReadFile()
    # push contents of data
    value_range = {
        "values": [
            ["hour-min-sec", "wifi_speed(Mbps)"]
        ]
    }
    response = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range="'Wifi_Speed_Test'!A1:B1",
        valueInputOption="RAW",
        body=value_range
    ).execute()

    # push data
    value = [[entry.time, entry.speed] for entry in speedList]
    value_range = {
        "values": value
    }
    update_range = f"'Wifi_Speed_Test'!A2:B{int(len(value)) + 1}"
    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=update_range,
        valueInputOption="RAW",
        body=value_range
    ).execute()
    SendMail()


def Main():
    global runLoop
    ScheduleTime()

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    if emailSender != None and passwordSender != None and emailSender != None:
        Main()