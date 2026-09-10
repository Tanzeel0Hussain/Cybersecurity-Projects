from pathlib import Path
import os
import secrets

from flask import Flask, render_template, redirect, url_for, session, request, flash
from werkzeug.utils import secure_filename

from auth import auth_bp, initialize_database
from log_analysis import analyze_logs, generate_report
from risk_engine import calculate_threat, generate_threat_report
from alert_system import generate_alerts

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
UPLOAD_DIR = BASE_DIR / "uploads"
REPORT_DIR = BASE_DIR / "reports"
ALERT_DIR = BASE_DIR / "alerts"
ALLOWED_EXTENSIONS = {"log", "txt"}

app = Flask(
    __name__,
    template_folder=str(PROJECT_DIR / "templates"),
    static_folder=str(PROJECT_DIR / "static"),
)
app.config.update(
    SECRET_KEY=os.environ.get("SECRET_KEY") or secrets.token_hex(32),
    MAX_CONTENT_LENGTH=2 * 1024 * 1024,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)
app.register_blueprint(auth_bp)

for directory in (UPLOAD_DIR, REPORT_DIR, ALERT_DIR):
    directory.mkdir(parents=True, exist_ok=True)
initialize_database()


def login_required():
    return "user" in session


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def current_log_file():
    saved = session.get("latest_log")
    if saved:
        candidate = UPLOAD_DIR / saved
        if candidate.is_file():
            return candidate

    files = [path for path in UPLOAD_DIR.iterdir() if path.is_file()]
    return max(files, key=lambda path: path.stat().st_mtime) if files else None


@app.route("/")
def home():
    return redirect(url_for("dashboard" if login_required() else "auth.login"))


@app.route("/dashboard")
def dashboard():
    if not login_required():
        return redirect(url_for("auth.login"))
    return render_template("dashboard.html", user=session["user"])


@app.route("/upload_logs", methods=["GET", "POST"])
def upload_logs():
    if not login_required():
        return redirect(url_for("auth.login"))

    message = ""
    if request.method == "POST":
        file = request.files.get("logfile")
        if not file or not file.filename:
            flash("Choose a log file first.", "error")
            return render_template("upload_logs.html", message="")

        if not allowed_file(file.filename):
            flash("Only .log and .txt files are accepted.", "error")
            return render_template("upload_logs.html", message="")

        filename = secure_filename(file.filename)
        if not filename:
            flash("Invalid filename.", "error")
            return render_template("upload_logs.html", message="")

        save_path = UPLOAD_DIR / filename
        file.save(save_path)
        session["latest_log"] = filename

        ip_counter, user_counter = analyze_logs(str(save_path))
        report_path = REPORT_DIR / "analysis_report.txt"
        generate_report(str(save_path), ip_counter, user_counter, str(report_path))
        message = f"Analysis complete. Report saved as {report_path.name}."

    return render_template("upload_logs.html", message=message)


@app.route("/threat_report")
def threat_report():
    if not login_required():
        return redirect(url_for("auth.login"))

    log_file = current_log_file()
    if log_file is None:
        return render_template("upload_logs.html", message="Please upload and analyze logs first.")

    ip_counter, user_counter = analyze_logs(str(log_file))
    threat_summary = calculate_threat(ip_counter, user_counter)
    report_path = REPORT_DIR / "threat_report.txt"
    generate_threat_report(threat_summary, str(report_path))

    return render_template("threat_report.html", threat=threat_summary, report_path=report_path.name)


@app.route("/alerts")
def alerts():
    if not login_required():
        return redirect(url_for("auth.login"))

    log_file = current_log_file()
    if log_file is None:
        return render_template("upload_logs.html", message="Please upload and analyze logs first.")

    ip_counter, user_counter = analyze_logs(str(log_file))
    threat_summary = calculate_threat(ip_counter, user_counter)
    alerts_list, alert_file = generate_alerts(threat_summary, str(ALERT_DIR))
    message = f"Alerts saved as {Path(alert_file).name}." if alert_file else "No high-risk alerts."

    return render_template("alerts.html", alerts=alerts_list, message=message)


@app.errorhandler(413)
def too_large(_error):
    return "Upload too large. Maximum size is 2 MB.", 413


if __name__ == "__main__":
    app.run()
