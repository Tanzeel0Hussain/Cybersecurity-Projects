from pathlib import Path
from flask import Flask, render_template, request, abort
import json
from datetime import datetime, timezone

BASE_DIR = Path(__file__).resolve().parent
REPORTS_FILE = BASE_DIR / "data" / "reports.json"

app = Flask(__name__)


def calculate_risk(answers):
    if len(answers) != 4:
        raise ValueError("All assessment questions must be answered.")

    allowed_values = {"0", "2", "3"}
    if any(answer not in allowed_values for answer in answers):
        raise ValueError("Invalid assessment response.")

    score = sum(int(answer) for answer in answers)

    if score <= 5:
        return score, "Low Risk", "green"
    if score <= 10:
        return score, "Medium Risk", "orange"
    return score, "High Risk", "red"


def load_reports():
    try:
        with REPORTS_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/quiz")
def quiz():
    return render_template("quiz.html")


@app.route("/report", methods=["POST"])
def report():
    answers = request.form.getlist("q")

    try:
        score, level, color = calculate_risk(answers)
    except ValueError as exc:
        abort(400, description=str(exc))

    REPORTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    reports = load_reports()
    reports.append(
        {
            "score": score,
            "level": level,
            "date": datetime.now(timezone.utc).isoformat(timespec="minutes"),
        }
    )

    with REPORTS_FILE.open("w", encoding="utf-8") as file:
        json.dump(reports, file, indent=2)

    return render_template("report.html", score=score, level=level, color=color)


if __name__ == "__main__":
    app.run()
