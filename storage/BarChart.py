import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta

class BarChart():
    hourly_avg_speed = [None] * 24
    hourly_max_speed = [None] * 24
    hourly_min_speed = [None] * 24
    hours_str = [None]
    hours_int = [None]

    # get hour list from 24h ago to current time
    @classmethod
    def getHours(cls):
        cls.hours_str.clear()
        cls.hours_int.clear()
        currentTime = datetime.now()
        for i in range(24):
            previousHour = currentTime - timedelta(hours=i)

            cls.hours_str.append(str(previousHour.hour))
        cls.hours_str.reverse()

        for i in range(24):
            previousHour = currentTime - timedelta(hours=i)

            cls.hours_int.append(previousHour.hour)
        cls.hours_int.reverse()
        print(cls.hours_int)

    # main function
    @classmethod
    def run(cls):
        cls.hourly_avg_speed.clear()
        cls.hourly_max_speed.clear()
        cls.hourly_min_speed.clear()

        cls.getHours()
        cls.getSpeedFromDb()
        cls.createBarChart()
        cls.dataTip()

        plt.savefig(f'barchart/{cls.getFileName()}.png', dpi=300)
        plt.close()

    # get file name follow date
    @classmethod
    def getFileName(cls):
        return datetime.now().strftime("%Y-%m-%d")

    # get speed from database and get avg, max, min speed
    @classmethod
    def getSpeedFromDb(cls):
        # Kết nối đến cơ sở dữ liệu SQLite
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

        # Chuyển cột "timestamp" thành kiểu thời gian
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        print(df)
        
        # Phân nhóm dữ liệu theo giờ và tính tốc độ trung bình, tối đa và tối thiểu mỗi giờ
        for hour in cls.hours_int:
            data_hour = df[df['timestamp'].dt.hour == hour]
            if not data_hour.empty:
                hourly_avg = data_hour['speed'].mean()
                hourly_max = data_hour['speed'].max()
                hourly_min = data_hour['speed'].min()
            else:
                hourly_avg = 0
                hourly_max = 0
                hourly_min = 0
            cls.hourly_avg_speed.append(hourly_avg)
            cls.hourly_max_speed.append(hourly_max)
            cls.hourly_min_speed.append(hourly_min)

        print(cls.hourly_avg_speed)

    @classmethod 
    def Table(cls):
        cls.hourly_avg_speed = [round(value, 1) for value in cls.hourly_avg_speed]
        # filterData = [(hour, speed) for hour, speed in zip(cls.hours_str, cls.hourly_avg_speed) if speed != 0]
        # data = {
        #     'Hour': [hour for hour, _ in filterData],
        #     'Avg Speed': [speed for _, speed in filterData],
        # }
        data = {"hour": cls.hours_str, "avg speed": cls.hourly_avg_speed}
        df = pd.DataFrame(data)

        return df.to_html(index=False, escape=False)

    @classmethod
    def createBarChart(cls):
        colors = []
        for speed in cls.hourly_avg_speed:
            if speed >= 100:
                colors.append('green')
            elif speed > 20:
                colors.append('orange')
            else:
                colors.append('#8B0000')

        plt.figure(figsize=(16, 9))
        plt.bar(cls.hours_str, cls.hourly_avg_speed, color=colors)

        plt.axhline(y=100, color='red', linestyle='-', linewidth=1)
        plt.axhline(y=20, color='red', linestyle='-', linewidth=1)


        plt.xlabel('Hour')
        plt.ylabel('Avg speed (Mbps)')
        plt.xticks(cls.hours_str, cls.hours_str)
        plt.grid(True)

    @classmethod
    def dataTip(cls):
        for i in range(len(cls.hours_str)):
            avg_speed = cls.hourly_avg_speed[i]
            max_speed = cls.hourly_max_speed[i]
            min_speed = cls.hourly_min_speed[i]
            hour = cls.hours_str[i]

            if avg_speed == 0:
                text = ''
            else:
                text = f'Mx{max_speed:.0f}\nMn{min_speed:.0f}'

            plt.annotate(text, (hour, avg_speed), textcoords="offset points", xytext=(0, 5), ha='center')

if __name__ == "__main__":
    BarChart.run()
