import sqlite3
import pandas as pd
from datetime import datetime, timedelta

class DataBase():
    speed = []
    time = []

    def loadDb(time, speed):
        # Kết nối đến cơ sở dữ liệu SQLite
        conn = sqlite3.connect('network_speed.db')
        cursor = conn.cursor()

        # Tạo bảng network_speed nếu nó chưa tồn tại
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS network_speed (
                id INTEGER PRIMARY KEY,
                timestamp TIMESTAMP,
                speed REAL
            )
        ''')

        cursor.execute(
            "INSERT INTO network_speed (timestamp, speed) VALUES (?, ?)",
            (time, speed)
        )
        conn.commit()


        conn.close()

    def readDb():
        DataBase.time.clear()
        DataBase.speed.clear()

        conn = sqlite3.connect('network_speed.db')

        # Định dạng thời gian hiện tại
        current_time = datetime.now()

        # Tính thời gian 24 giờ trước
        time_24_hours_ago = current_time - timedelta(hours=24)

        # Tạo câu truy vấn SQL để lấy dữ liệu trong khoảng thời gian
        query = f"SELECT * FROM network_speed WHERE timestamp >= '{time_24_hours_ago}' AND timestamp <= '{current_time}'"

        # Đọc dữ liệu vào DataFrame
        df = pd.read_sql_query(query, conn)

        # Đóng kết nối đến cơ sở dữ liệu
        conn.close()

        DataBase.time = list(df['timestamp'])
        DataBase.speed = list(df['speed'])

        conn.close()

DataBase.readDb()
