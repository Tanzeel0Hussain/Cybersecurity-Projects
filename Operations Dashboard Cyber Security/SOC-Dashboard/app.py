from flask import Flask, render_template, redirect, url_for, session, request
from auth import auth_bp
from log_analysis import analyze_logs, generate_report
from risk_engine import calculate_threat, generate_threat_report
from alert_system import generate_alerts
import os

# --- Flask App Setup ---
app = Flask(__name__)
app.secret_key = "soc_dashboard_secret_key"
app.register_blueprint(auth_bp)

# --- Routes ---

# Home
@app.route("/")
def home():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("auth.login"))

# Dashboard
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("auth.login"))
    return render_template("dashboard.html", user=session["user"])

# --- Phase 2: Upload Logs ---
@app.route("/upload_logs", methods=["GET", "POST"])
def upload_logs():
    if "user" not in session:
        return redirect(url_for("auth.login"))

    message = ""
    if request.method == "POST":
        file = request.files.get("logfile")
        if file:
            save_path = os.path.join("uploads", file.filename)
            os.makedirs("uploads", exist_ok=True)
            file.save(save_path)

            ip_counter, user_counter = analyze_logs(save_path)
            report_path = generate_report(save_path, ip_counter, user_counter)
            message = f"Analysis complete. Report saved at {report_path}"

    return render_template("upload_logs.html", message=message)

# --- Phase 3: Threat Report ---
@app.route("/threat_report")
def threat_report():
    if "user" not in session:
        return redirect(url_for("auth.login"))

    # Ensure logs exist
    if not os.path.exists("uploads") or not os.listdir("uploads"):
        message = "Please upload and analyze logs first."
        return render_template("upload_logs.html", message=message)

    log_file = os.path.join("uploads", os.listdir("uploads")[0])
    ip_counter, user_counter = analyze_logs(log_file)
    threat_summary = calculate_threat(ip_counter, user_counter)
    report_path = generate_threat_report(threat_summary)

    return render_template("threat_report.html", threat=threat_summary, report_path=report_path)

# --- Phase 4: Alerts ---
@app.route("/alerts")
def alerts():
    if "user" not in session:
        return redirect(url_for("auth.login"))

    if not os.path.exists("uploads") or not os.listdir("uploads"):
        message = "Please upload and analyze logs first."
        return render_template("upload_logs.html", message=message)

    log_file = os.path.join("uploads", os.listdir("uploads")[0])
    ip_counter, user_counter = analyze_logs(log_file)
    threat_summary = calculate_threat(ip_counter, user_counter)
    
    alerts_list, alert_file = generate_alerts(threat_summary)
    message = f"Alerts saved at {alert_file}" if alert_file else "No high-risk alerts."

    return render_template("alerts.html", alerts=alerts_list, message=message)

# --- Run App ---
if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    os.makedirs("alerts", exist_ok=True)
    app.run(debug=True)
