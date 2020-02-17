from datetime import datetime
from parser import parse_date_str

from flask import Flask, render_template, jsonify, request


app = Flask(__name__)


def format_now():
    return datetime.now().strftime("%a %d %b %Y %I:%M%p")

@app.route('/')
def index():
    return render_template("strftime.html", now_date=format_now())


@app.route("/format", methods=["POST"])
def format():
    dt = request.form["dateFormat"]
    formatted = parse_date_str(dt)
    if not formatted:
        return "", 400
    return jsonify({"message": formatted})


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)