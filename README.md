# 🔐 PASSFORT

A local, encrypted password manager built with Python and PySide6.

## Features
- Store credentials — title, username, password, and URL
- Encryption of all stored data
- Master password
- Search across saved entries
- One-click copy to clipboard

## Planned
- Auto-lock on inactivity
- Built-in password generator
- SQLite storage with encrypted data at rest
- Password strength indicator (zxcvbn)
- Show/hide password toggle
- Export vault
- Browser autofill (experimental)

## Tech stack
| | |
|---|---|
| Language | Python 3.x |
| GUI | PySide6 |
| Storage | SQLite (sqlite3) |
| Encryption | cryptography |
| Clipboard | pyperclip |
| Generator / Strength | secrets + zxcvbn |

## Getting started
```sh
pip install PySide6 cryptography pyperclip zxcvbn
apt install python3-argon2
cd src
python3 main.py
```
