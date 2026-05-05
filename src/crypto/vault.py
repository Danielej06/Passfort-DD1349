import json
import base64
import os

from kdf import derive_key, create_key_from_password
from aes import encrypt, decrypt

# Konvertera bytes till Base64 string.
def bytes_to_base64(data: bytes) -> str:
    b64_bytes = base64.b64encode(data)

    return b64_bytes.decode("utf-8")
# Invers av ovan funktion. Konverterar Base64 string till bytes.
def base64_to_bytes(data: str) -> bytes:
    return base64.b64decode(data)
# Skapar en empty vault
def create_vault() -> dict:
    return {}
 # Sparar vaulten säkert. Skriver enkrypterade datan in i vår vault.
def save_vault(vault: dict, password: str, file_path: str = "data.json") -> None:

    key, salt = create_key_from_password(password)
    vault_json = json.dumps(vault, indent = 4)
    vault_bytes = vault_json.encode("utf-8")
    encrypted_payload = encrypt(vault_bytes, key)

    file_data = {
        "salt": bytes_to_base64(salt),
        "nonce": bytes_to_base64(encrypted_payload["nonce"]),
        "ciphertext": bytes_to_base64(encrypted_payload["ciphertext"]),
    }

    with open(file_path, "w") as file:
        json.dump(file_data, file, indent = 4)

# Invers till save vault. Gör motsatt steg för att sedan ta fram faktiska dekrypterade vaulten.
def load_vault(password: str, file_path: str = "data.json") -> dict:
    if not os.path.exists(file_path):
        return create_vault()

    with open(file_path, "r") as file:
        file_data = json.load(file)

    salt = base64_to_bytes(file_data["salt"])
    nonce = base64_to_bytes(file_data["nonce"])
    ciphertext = base64_to_bytes(file_data["ciphertext"])

    key = derive_key(password, salt)

    encrypted_payload = {
        "nonce": nonce,
        "ciphertext": ciphertext,
    }

    vault_bytes = decrypt(encrypted_payload, key)
    vault_json = vault_bytes.decode("utf-8")
    vault = json.loads(vault_json)
    return vault


