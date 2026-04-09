from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Dockerized Application Version 2 is running successfully!"

@app.route("/health")
def health():
    return {"status": "ok", "message": "Application is healthy"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
