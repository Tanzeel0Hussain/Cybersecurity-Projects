# 📊 Log Analyzer (Security & Forensics Tool)

An advanced Python-based log analysis tool designed for Blue Team operations.
This project analyzes authentication logs to detect brute-force attacks and suspicious behavior.

---

## 🚀 What This Project Can Do
- Analyze authentication log files
- Detect failed login attempts
- Identify suspicious IP addresses
- Detect brute-force attack patterns
- Find most targeted usernames
- Generate a security report automatically
- Display color-coded terminal output

---

## 🧠 Why This Project Is ADVANCED
✔ Focuses on Blue Team & SOC operations  
✔ Uses real server authentication logs  
✔ Detects real-world attack behavior  
✔ Applies pattern recognition & thresholds  
✔ Used in cybersecurity monitoring & forensics  

This project goes beyond scanning and attacking —  
it focuses on **detection, monitoring, and defense**.

---

## 🛠 Requirements

pip install colorama
pip install colorama requests

---

## ▶️ How to Run

python log_analyzer.py

---

## 📁 Required Log File

auth.log  
→ Linux authentication log or sample SSH log file

---

## 📁 Output File

security_report.txt

---

## ⚙️ How It Works
1. Reads authentication log file
2. Extracts IP addresses & usernames
3. Counts failed login attempts
4. Flags suspicious IPs using threshold
5. Generates a detailed security report

---

## ⚠️ Legal Disclaimer
This project is created for:
✔ Educational use  
✔ SOC & Blue Team training  
✔ Digital forensics labs  

Do NOT analyze logs without permission.

---

## 🔮 Future Enhancements
- CSV / JSON export
- Real-time log monitoring
- Geo-IP lookup
- GUI dashboard
- Email alert system

---

⭐ If you like this project, give the repository a star!
