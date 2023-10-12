import time
import smtplib
import os

from datetime import datetime, timedelta
from storage.EmailFile import EmailFile
from storage.Other import Other
from storage.BarChart import BarChart

from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders

class Mail(Other):
    emailSender = "speed-test@liva.com.vn"
    passwordSender = "#&u){13e7$m_"
    serverMail = "mail.liva.com.vn"
    port = 2525

    def SendMail():
        EmailFile.readFile()
        if len(EmailFile.emailReceivers) > 0:
            mailName = Other.GetTodayName()
            BarChart.run()

            for i in range(len(EmailFile.emailReceivers)):
                while True:
                    if Other.IsInternetAvailable():
                        msg = MIMEMultipart()
                        Mail.CreateMailStructure(msg, i, mailName)
                        Mail.ConnectServer(msg, i)
                        break
                    else:
                        print("no internet connection, wait 1 minute to try again")
                        time.sleep(60)
            os.remove(f"barchart/{mailName}.png")
        else:
            print("no data in email_receivers.txt")
    
    def CreateMailStructure(msg, emailReceiverNumb, mailName):

        subject = f"Wifi Speed Test {Other.GetTodayName()}"
        currentTime = datetime.now()
        time24HoursAgo = currentTime - timedelta(hours=24)
        currentTime = currentTime.strftime("%Y-%m-%d %Hh")
        time24HoursAgo = time24HoursAgo.strftime("%Y-%m-%d %Hh")
        message = f" Dear customer!\n This is your wifi speed test result in the last 24 hours from ({time24HoursAgo}) to ({currentTime}). Down there are a data table and a barchart."

        msg["From"] = Mail.emailSender
        msg["To"] = EmailFile.emailReceivers[emailReceiverNumb]
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))
        Mail.attachPng(msg, mailName)
        html_part = MIMEText(BarChart.Table(), 'html')
        msg.attach(html_part)
    
    def attachPng(msg, mailName):
        filePath = f"{mailName}.png"

        attachment = open(f"barchart/{filePath}", 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= " + filePath)
        msg.attach(part)
        attachment.close()

    def ConnectServer(msg, emailReceiverNumb):
        try:
            print("connecting to sever...")
            server = smtplib.SMTP(Mail.serverMail, Mail.port)
            server.starttls()
            server.login(Mail.emailSender, Mail.passwordSender)
            print("connected to sever")
            server.sendmail(Mail.emailSender, EmailFile.emailReceivers[emailReceiverNumb], msg.as_string())
            print("sent mail")
            server.quit()
        except Exception as e:
            print("error sending", str(e))

if __name__ == "__main__":
    Mail.SendMail()