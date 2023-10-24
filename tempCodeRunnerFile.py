    load_dotenv()
        newPort = os.getenv("FLASK_PORT")
        if port != newPort:
            print(port)
            print(newPort)
            os.kill(os.getpid(), signal.SIGTERM)
            port = newPort
            app = Flask(__name__, static_folder='static')
            app.run(port=int(port))
        time.sleep(1)