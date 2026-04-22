# 🔐 PASSFORT

A local, encrypted password manager built with Python and PySide6.

## Features
- Store credentials — title, username, password, and URL
- Encryption of all stored data
- Master password + auto-lock on inactivity
- Search across saved entries
- One-click copy to clipboard
- Built-in password generator

## Planned
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
python main.py
```
