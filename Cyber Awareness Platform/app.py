from flask import Flask, render_template, request
import json
from datetime import datetime

app = Flask(__name__)

def calculate_risk(answers):
    score = 0
    for ans in answers:
        score += int(ans)

    if score <= 5:
        level = "Low Risk"
        color = "green"
    elif score <= 10:
        level = "Medium Risk"
        color = "orange"
    else:
        level = "High Risk"
        color = "red"

    return score, level, color

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/quiz")
def quiz():
    return render_template("quiz.html")

@app.route("/report", methods=["POST"])
def report():
    answers = request.form.getlist("q")
    score, level, color = calculate_risk(answers)

    report_data = {
        "score": score,
        "level": level,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    try:
        with open("data/reports.json", "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(report_data)

    with open("data/reports.json", "w") as f:
        json.dump(data, f, indent=4)

    return render_template("report.html", score=score, level=level, color=color)

if __name__ == "__main__":
    app.run(debug=True)
