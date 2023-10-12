import os
import time

from storage.Other import Other

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from storage.DataBase import DataBase

class Sheet:
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    SPREADSHEET_ID = "19zWNRUC1pLfVSpV5IEHP1tcV_Ptvu0F032xad4iG_WE"
    def RunSheet():
        while True:
            if Other.IsInternetAvailable():
                try:
                    credentials = None
                    if os.path.exists("token.json"):
                        credentials = Credentials.from_authorized_user_file("token.json", Sheet.SCOPES)
                    if not credentials or not credentials.valid:
                        if credentials and credentials.expired and credentials.refresh_token:
                            credentials.refresh(Request())
                        else:
                            flow = InstalledAppFlow.from_client_secrets_file("credential.json", Sheet.SCOPES)
                            credentials = flow.run_local_server(port=0)
                        with open("token.json", "w") as token:
                            token.write(credentials.to_json())
                    Sheet.CreateSheet(credentials)
                    break
                except HttpError as error:
                    print(error)
            else:
                print("no internet to runSheet, wait 1 minute to try again")
                time.sleep(60)

    def CreateSheet(credentials):
            service = build("sheets", "v4", credentials=credentials)
            # create google sheet file
            spreadsheet_body = {
                "properties": {
                    "title": Other.GetTodayName()
                }
            }

            sheets = service.spreadsheets().create(body=spreadsheet_body)
            response = sheets.execute()
            Sheet.SPREADSHEET_ID = response["spreadsheetId"]

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
                spreadsheetId=Sheet.SPREADSHEET_ID,
                body=worksheet_body
            ).execute()
            Sheet.pushToSheet(service)

    def pushToSheet(service):
        # push contents of data
        value_range = {
            "values": [
                ["hour-min-sec", "wifi_speed(Mbps)"]
            ]
        }
        response = service.spreadsheets().values().update(
            spreadsheetId=Sheet.SPREADSHEET_ID,
            range="'Wifi_Speed_Test'!A1:B1",
            valueInputOption="RAW",
            body=value_range
        ).execute()
        
        # push data
        DataBase.readDb()
        value = []
        for i in range(len(DataBase.time)):
            value.append([DataBase.time[i], DataBase.speed[i]])

        print(f"{value}")
        value_range = {
            "values": value
        }
        update_range = f"'Wifi_Speed_Test'!A2:B{int(len(value)) + 1}"
        service.spreadsheets().values().update(
            spreadsheetId=Sheet.SPREADSHEET_ID,
            range=update_range,
            valueInputOption="RAW",
            body=value_range
        ).execute()
def main():
    Sheet.RunSheet()
if __name__ == "__main__":
    main()