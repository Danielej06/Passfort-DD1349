## This file is responsible for creating, saving and loading the vault. The vault is where all the credentials are stored. The vault is encrypted with the master password and can only be decrypted with the master password. 
## The vault is stored in a file called data.db. The vault is a dictionary where the key is the title of the credential and the value is another dictionary with the username and password.
import base64
import os
import sqlite3
con = sqlite3.connect("data.db")
cur = con.cursor()

from crypto.aes import encrypt, decrypt
from crypto.kdf import derive_key, create_key_from_password

# Konvertera bytes till Base64 string.
def bytes_to_base64(data: bytes) -> str:
    b64_bytes = base64.b64encode(data)

    return b64_bytes.decode("utf-8")
# Invers av ovan funktion. Konverterar Base64 string till bytes.
def base64_to_bytes(data: str) -> bytes:
    return base64.b64decode(data)
# Skapar en empty vault
def create_vault() -> dict:
    SQL = "CREATE TABLE IF NOT EXISTS vault (id INTEGER PRIMARY KEY, URL TEXT NOT NULL," 
    SQL += "username TEXT NOT NULL, cipheredpassword TEXT NOT NULL, salt TEXT NOT NULL, nonce TEXT NOT NULL)"
    cur.execute(SQL)
    con.commit()
    return {}
 
 # Sparar vaulten säkert. Skriver enkrypterade datan in i vår vault.
def save_vault(vault: dict, password: str) -> None:
    key, salt = create_key_from_password(password)
    password_bytes = vault["password"].encode("utf-8")
    encrypted_payload = encrypt(password_bytes, key)

    SQL = "INSERT INTO vault (URL, username, cipheredpassword, salt, nonce) VALUES (?, ?, ?, ?, ?)"
    cur.execute(SQL, (vault["url"], vault["username"], bytes_to_base64(encrypted_payload["ciphertext"]), bytes_to_base64(salt), bytes_to_base64(encrypted_payload["nonce"])))
    con.commit()

def update_vault(vault: dict, password: str, id: int) -> None:
    key, salt = create_key_from_password(password)
    password_bytes = vault["password"].encode("utf-8")
    encrypted_payload = encrypt(password_bytes, key)

    SQL = "UPDATE vault SET URL = ?, username = ?, cipheredpassword = ?, salt = ?, nonce = ? WHERE ID = ?"
    cur.execute(SQL, (vault["url"], vault["username"], bytes_to_base64(encrypted_payload["ciphertext"]), bytes_to_base64(salt), bytes_to_base64(encrypted_payload["nonce"]), id))
    con.commit()
    
def vault_exists() -> bool:
    return os.stat("data.db").st_size != 0

def check_vault_accessible(password: str) -> bool:
    try:
        load_vault(password, 1)
        return True
    except Exception:
        return False

def load_urls() -> list:
    SQL = "SELECT URL, username FROM vault"
    ## ISSUE: Fix so that it doesnt crash if there are no credentials saved yet, instead return an empty list and print a message in read_credentials.py that there are no credentials saved yet.
    res = cur.execute(SQL)
    rows = res.fetchall()

    urls = []
    for row in rows:
        urls.append((row[0], row[1]))

    return urls

# Invers till save vault. Gör motsatt steg för att sedan ta fram faktiska dekrypterade vaulten.
def load_vault(password: str, id: int) -> dict:
    
    SQL = "SELECT url, username, cipheredpassword, salt, nonce FROM vault WHERE ID = ?"
    res = cur.execute(SQL, (id,))
    rows = res.fetchall()

    if not rows:
        return create_vault()

    vaults = []
    for row in rows:
        salt = base64_to_bytes(rows[0][3])
        nonce = base64_to_bytes(rows[0][4])
        ciphertext = base64_to_bytes(rows[0][2])
        
        key = derive_key(password, salt)

        encrypted_payload = {
            "nonce": nonce,
            "ciphertext": ciphertext,
        }

        password_bytes = decrypt(encrypted_payload, key)
        retreived_password = password_bytes.decode("utf-8")
        vaults = {
            "url": rows[0][0],
            "username": rows[0][1],
            "password": retreived_password
        }

    return vaults
