# 🔑 Password Cracker (Offline Hash Demo)

An offline dictionary-matching project for learning how weak password hashes can be recovered when a matching word is present in a local wordlist.

## Supported demonstrations
- MD5
- SHA-1
- SHA-256

## Included files
- `password_cracker.py`
- `hashes.txt` — safe sample hashes
- `wordlist.txt` — small sample wordlist
- `requirements.txt`

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
python password_cracker.py
```

The program reads only local files and writes successful demo matches to `cracked_passwords.txt`.

## Security note
MD5 and SHA-1 are unsuitable for modern password storage. Real applications should use a dedicated password-hashing function such as Argon2, scrypt, bcrypt or PBKDF2 with appropriate configuration.

## Ethical use
Use only with hashes you own or have explicit authorization to test.
