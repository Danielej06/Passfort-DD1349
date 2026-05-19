# 🔐 Passfort

A local, encrypted password manager built with Python and Tkinter. All credentials are stored on your machine — no cloud, no third-party servers.


---

## Features

- Store credentials — title, username, password, and URL
- Encryption of all stored data
- Master password
- Search across saved entries
- Auto-lock on inactivity
- Built-in password generator
- SQLite storage with encrypted data at rest
- Password strength indicator
- Show/hide password toggle

## Demo

> _Screenshot or GIF here_

---

## Requirements

- Python 3.x
- `python3-argon2`
- `tkinter`
- `pyperclip`
- `zxcvbn`

On Debian/Ubuntu, install the system dependency:

```bash
apt install python3 python3-argon2
```

Then install Python dependencies:

```bash
pip install sqlite3 tkinter zxcvbn cryptography
```

## Installation

```bash
git clone https://github.com/Danielej06/Passfort-DD1349.git
cd Passfort-DD1349/src
python3 gui.py
```

Or download the latest release from the [Releases page](https://github.com/Danielej06/Passfort-DD1349/releases).

---

## Usage

1. Launch the app with `python3 gui.py`
2. Set a master password on first run — this encrypts your entire vault
3. Add entries with a title, username, password, and optional URL
4. Use the search bar to filter entries
5. Click the copy icon to copy a password to clipboard

---

## Tech Stack

| Component         | Technology                    |
|-------------------|-------------------------------|
| Language          | Python 3.x                    |
| GUI + Clipboard   | tkinter                       |
| Storage           | SQLite (`sqlite3`)            |
| Encryption        | `cryptography` + Argon2       |

---

## Project Structure

```
Passfort-DD1349/
├── src/          # Application source code
├── docs/         # Documentation
├── .gitignore
└── README.md
```

---

## Roadmap

- [ ] Auto-lock on inactivity
- [ ] Built-in password generator
- [ ] Password strength indicator
- [ ] Show/hide password toggle
- [ ] Export vault
- [ ] Browser autofill (experimental)

---

## Authors

- [Danielej06](https://github.com/Danielej06) and contributors

## License

This project was created as part of **DD1349 – Introduktion till datalogi** at KTH Royal Institute of Technology.
