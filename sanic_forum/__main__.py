from sanic_forum import app

if __name__ == "__main__":
    server = app.create()
    server.run(host="0.0.0.0", port=8000, debug=server.config.DEBUG)
