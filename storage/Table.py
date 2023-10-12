import sqlite3
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta

# Kết nối cơ sở dữ liệu SQLite
conn = sqlite3.connect('network_speed.db')

# Lấy dữ liệu từ cơ sở dữ liệu
currentTime = datetime.now()
time24HoursAgo = currentTime - timedelta(hours=24)
query = f"SELECT * FROM network_speed WHERE timestamp >= '{time24HoursAgo}' AND timestamp <= '{currentTime}'"
df = pd.read_sql_query(query, conn)

# Chuyển đổi DataFrame thành chuỗi HTML
html_table = df.to_html(index=False)

# Tạo email
from_email = 'speed-test@liva.com.vn'
to_email = 'huylexuan2911@gmail.com'
msg = MIMEMultipart()
msg['From'] = from_email
msg['To'] = to_email
msg['Subject'] = 'Dữ liệu từ cơ sở dữ liệu SQLite'

# Thêm nội dung email và đính kèm bảng HTML
body = MIMEText('Xin chào, đây là dữ liệu từ cơ sở dữ liệu của bạn:')
msg.attach(body)

html_part = MIMEText(html_table, 'html')
msg.attach(html_part)

# Kết nối đến máy chủ email và gửi email
smtp_server = 'mail.liva.com.vn'
smtp_port = 2525
smtp_username = 'speed-test@liva.com.vn'
smtp_password = '#&u){13e7$m_'

server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
server.login(smtp_username, smtp_password)
server.sendmail(from_email, to_email, msg.as_string())
server.quit()
