from version_handler import get_app

app = get_app()

if __name__ == "__main__":
    app.run(port=5000)
