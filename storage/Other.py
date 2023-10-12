import requests

from datetime import datetime

class Other():
    def IsInternetAvailable():
        try:
            requests.get("http://www.google.com", timeout=5)
            return True
        except requests.ConnectionError:
            return False
        
    def BitsToMb(sizeBits):
        sizeMb = round(sizeBits / (1024 * 1024), 2)
        return sizeMb
        
    def GetTodayName():
        today = datetime.now().strftime("%Y-%m-%d")
        return f"{today}"
    
    def convertStrToTime(value):
        time_format = "%Y-%m-%d %H:%M:%S"
        return datetime.strptime(value, time_format)