from app_inn import app

if __name__ == "__main__":
    from app import server as application
    application = app.server
    application.run()