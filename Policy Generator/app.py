from flask import Flask, render_template, request
import json
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    company = request.form["company"]
    industry = request.form["industry"]
    size = request.form["size"]

    policy = f"""
Cyber Security Policy
Company: {company}
Industry: {industry}
Company Size: {size}

1. Purpose
This policy ensures protection of company data and systems.

2. Access Control
Only authorized users may access systems.

3. Password Policy
Strong passwords with regular rotation are mandatory.

4. Incident Response
All incidents must be reported immediately.

5. Compliance
Company follows cyber security laws and best practices.
"""

    record = {
        "company": company,
        "industry": industry,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "policy": policy
    }

    try:
        with open("data/policies.json", "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(record)

    with open("data/policies.json", "w") as f:
        json.dump(data, f, indent=4)

    return render_template("policy.html", policy=policy)

if __name__ == "__main__":
    app.run(debug=True)
