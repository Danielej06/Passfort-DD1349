import hmac
import os
import sqlite3
from crypto.kdf import derive_key
from crypto.vault import base64_to_bytes, bytes_to_base64

con = sqlite3.connect("password.db")
cur = con.cursor()

def create_master_password()-> str:
    master_password = input("Enter your master password: ")
    # Two independent salts that make it safer to verify the master password without risking the security of the vault.
    # The verify_salt is used to create a key that is stored in the database and used to verify the master password. 
    # The enc_salt is used to create a key that is used to encrypt and decrypt the vault.
    verify_salt = os.urandom(16)
    enc_salt = os.urandom(16)
    
    verify_key = derive_key(master_password, verify_salt)
    
    SQL = """CREATE TABLE IF NOT EXISTS masterpassword (
        id INTEGER PRIMARY KEY,
        verify_key TEXT NOT NULL,
        verify_salt TEXT NOT NULL,
        enc_salt TEXT NOT NULL)"""
    cur.execute(SQL)
    con.commit()
    SQL = "INSERT INTO masterpassword (verify_key, verify_salt, enc_salt) VALUES ('"
    SQL += bytes_to_base64(verify_key) + "','" + bytes_to_base64(verify_salt) + "','" + bytes_to_base64(enc_salt) + "')"
    cur.execute(SQL)
    con.commit()
    print("Master password created successfully!")
    return master_password

def verify_master_password(master_password)-> bool:
    SQL = "SELECT * FROM masterpassword"
    cur.execute(SQL)
    row = cur.fetchone()
    if not row:
        return False
    stored_verify_key = base64_to_bytes(row[1])
    verify_salt = base64_to_bytes(row[2])
    enc_salt = base64_to_bytes(row[3])
    
    possible_key = derive_key(master_password, verify_salt)
    
    # Use hmac.compare_digest to prevent timing attacks. This will return False if the keys are not the same, and True if they are the same.
    if not hmac.compare_digest(possible_key, stored_verify_key):
        return None
    
    return derive_key(master_password, enc_salt)