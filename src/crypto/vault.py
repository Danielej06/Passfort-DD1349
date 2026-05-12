## This file is responsible for creating, saving and loading the vault. The vault is where all the credentials are stored. The vault is encrypted with the master password and can only be decrypted with the master password. 
## The vault is stored in a file called data.json. The vault is a dictionary where the key is the title of the credential and the value is another dictionary with the username and password.
import json
import base64
import os
import sqlite3
con = sqlite3.connect("tutorial.db")
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
    SQL = "CREATE TABLE IF NOT EXISTS vault (id INTEGER PRIMARY KEY, URL TEXT," 
    SQL += "username TEXT, cipheredpassword TEXT, salt TEXT, nonce TEXT)"
    cur.execute(SQL)
    con.commit()
    return {}
 
 # Sparar vaulten säkert. Skriver enkrypterade datan in i vår vault.
def save_vault(vault: dict, password: str) -> None:
    key, salt = create_key_from_password(password)
    password_bytes = vault["password"].encode("utf-8")
    encrypted_payload = encrypt(password_bytes, key)

    SQL = "INSERT INTO vault (URL, username, cipheredpassword, salt, nonce) VALUES ('"
    SQL += vault["URL"] + "','" + vault["username"] + "','" + bytes_to_base64(encrypted_payload["ciphertext"]) 
    SQL += "','" + bytes_to_base64(salt) + "','" + bytes_to_base64(encrypted_payload["nonce"]) + "')"
    cur.execute(SQL)
    con.commit()


# Invers till save vault. Gör motsatt steg för att sedan ta fram faktiska dekrypterade vaulten.
def load_vault(password: str) -> dict:
    
    SQL = "SELECT * FROM vault"
    cur.execute(SQL)
    rows = cur.fetchall()

    if not rows:
        return create_vault()

    vaults = []
    for row in rows:
        salt = base64_to_bytes(row[4])
        nonce = base64_to_bytes(row[5])
        ciphertext = base64_to_bytes(row[3])

        key = derive_key(password, salt)

        encrypted_payload = {
            "nonce": nonce,
            "ciphertext": ciphertext,
        }

        vault_bytes = decrypt(encrypted_payload, key)
        vault_json = vault_bytes.decode("utf-8")
        vault = json.loads(vault_json)
        vaults.append(vault)

    return vaults

