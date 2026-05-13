import sqlite3
from crypto.aes import encrypt, decrypt
from crypto.kdf import derive_key, create_key_from_password
from crypto.vault import base64_to_bytes, bytes_to_base64
con = sqlite3.connect("password.db")
cur = con.cursor()

def create_master_password()-> str:
    master_password = input("Enter your master password: ")
    key, salt = create_key_from_password(master_password)
    password_bytes = master_password.encode("utf-8")
    encrypted_payload = encrypt(password_bytes, key)
    SQL = "CREATE TABLE IF NOT EXISTS masterpassword (id INTEGER PRIMARY KEY, cipheredpassword TEXT, salt TEXT, nonce TEXT)"
    cur.execute(SQL)
    con.commit()
    SQL = "INSERT INTO masterpassword (cipheredpassword, salt, nonce) VALUES ('"
    SQL += bytes_to_base64(encrypted_payload["ciphertext"]) 
    SQL += "','" + bytes_to_base64(salt) + "','" + bytes_to_base64(encrypted_payload["nonce"]) + "')"
    cur.execute(SQL)
    con.commit()
    print("Master password created successfully!")
    return master_password

def verify_master_password(master_password)-> bool:
    try:
        SQL = "SELECT * FROM masterpassword"
        cur.execute(SQL)
        row = cur.fetchone()
        if not row:
            return False
        encrypted_password = base64_to_bytes(row[1])
        salt = base64_to_bytes(row[2])
        nonce = base64_to_bytes(row[3])
        
        encrypted_payload = {
        "nonce": nonce,
        "ciphertext": encrypted_password,
        }
        
        key = derive_key(master_password, salt)
        
        password_bytes = decrypt(encrypted_payload, key)
        retreived_password = password_bytes.decode("utf-8")
        return retreived_password == master_password
    except Exception:
        return False