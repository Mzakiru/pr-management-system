from flask import Flask, render_template
import os

app = Flask(__name__)

DATA_DIR = "data"

def read_data(file):
    path = os.path.join(DATA_DIR, file)
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines()]

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/activities")
def activities():
    data = read_data("activities.txt")
    return render_template("activities.html", records=data)

@app.route("/contacts")
def contacts():
    data = read_data("contacts.txt")
    return render_template("contacts.html", records=data)

@app.route("/events")
def events():
    data = read_data("events.txt")
    return render_template("events.html", records=data)

@app.route("/media")
def media():
    data = read_data("media.txt")
    return render_template("media.html", records=data)

if __name__ == "__main__":
    app.run(debug=True)
