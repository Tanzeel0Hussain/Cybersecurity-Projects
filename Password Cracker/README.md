# 🔓 Password Cracker (Hash-Based | Ethical)

An advanced Python-based password cracker that performs dictionary attacks on hashed passwords.
This project is designed for cybersecurity education, digital forensics, and ethical hacking labs.

---

## 🚀 What This Project Can Do
- Crack hashed passwords using dictionary attack
- Supports multiple hash algorithms:
  - MD5
  - SHA1
  - SHA256
- Matches hashes against large wordlists
- Displays cracked & failed hashes clearly
- Saves cracked passwords to file
- Works fully offline (no internet needed)

---

## 🧠 Why This Project Is ADVANCED
✔ Uses real-world cryptographic hashing algorithms  
✔ Demonstrates password security weaknesses  
✔ Simulates forensic & penetration testing scenarios  
✔ More complex logic than scanners or brute tools  
✔ Interview-level cybersecurity project  

Compared to basic tools, this project focuses on:
- Cryptography concepts
- Hashing vs plaintext passwords
- Security auditing techniques

---

## 🛠 Requirements

pip install colorama
pip install colorama requests

---

## ▶️ How to Run

python password_cracker.py

---

## 📁 Required Files

hashes.txt  
→ Contains password hashes (one per line)

wordlist.txt  
→ Contains possible passwords

---

## 📁 Output File

cracked_passwords.txt

---

## ⚙️ How It Works
1. Loads hashes & wordlist
2. Converts each word into selected hash
3. Compares hash values
4. Cracks matching passwords
5. Logs results to file

---

## ⚠️ Legal Disclaimer
This project is created ONLY for:
✔ Educational use  
✔ Cybersecurity labs  
✔ Digital forensics practice  

Do NOT use this tool to attack real systems or unauthorized data.

---

## 🔮 Future Enhancements
- Brute-force mode
- Rainbow table support
- GUI version
- Multi-threading
- Hash auto-detection

---

⭐ If you like this project, give the repository a star!
