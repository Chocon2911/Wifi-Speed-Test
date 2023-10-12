from flask import Flask, render_template, request, redirect, url_for
from storage.EmailFile import EmailFile

app = Flask(__name__, static_folder='static')

# Mật khẩu cho trang web
USERNAME = "toilaai"
PASSWORD = "29112004"
authenticated = False  # Biến để kiểm tra xác thực

@app.route('/', methods=['GET', 'POST'])
def Login():
    global authenticated

    error = None
    if request.method == 'POST':
        if not authenticated:
            username_attempt = request.form['username']
            password_attempt = request.form['password']
            if password_attempt == PASSWORD and username_attempt == USERNAME:
                authenticated = True  # Xác thực thành công

                return redirect(url_for('home'))
            else:
                error = "username or password is wrong!"

    return render_template('login.html', authenticated=authenticated, error=error)

@app.route('/home', methods=['GET', 'POST'])
def home():

    return render_template('home.html')

@app.route('/emailReceivers', methods=['GET', 'POST'])
def emailReceivers():
    if request.method == 'POST':
        emailReceivers = request.form['email_receivers'].split(', ')
        with open("data/email_receivers.txt", "w") as file:
            for email in emailReceivers:
                file.write(f"{email}\n")
        EmailFile.readFile()

    return render_template('emailReceivers.html')

@app.route('/loopTime', methods=['GET', 'POST'])
def loopTime():
    if request.method == 'POST':
        normal_runLoop = request.form['normal_runLoop']
        slow_runLoop = request.form['slow_runLoop']
        resting_runLoop = request.form['resting_runLoop']
        slow_speed = request.form['slow_speed']
        slow_speed_list = request.form['slow_speed_list']
        with open("data/loop_time.txt", "w") as file:
            file.write(f"{normal_runLoop}\n")
            file.write(f"{slow_runLoop}\n")
            file.write(f"{resting_runLoop}")
        with open("data/slow_speed.txt", "w") as file:
            file.write(f"{slow_speed}\n")
            file.write(f"{slow_speed_list}")

    return render_template('loopTime.html')

@app.route("/dailyTime", methods=['GET', 'POST'])
def dailyTime():
    if request.method == 'POST':
        with open("data/daily_time.txt", "w") as file:
            file.write(f"{request.form['daily_time']}")

    return render_template('dailyTime.html')

if __name__ == '__main__':
    app.run(debug=True)
