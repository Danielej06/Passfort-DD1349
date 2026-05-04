Take normal Python credential data
→ turn it into JSON bytes
→ encrypt it
→ base64 encode encrypted bytes
→ save to disk

Then later:

load encrypted JSON from disk
→ base64 decode bytes
→ derive key again from password + stored salt
→ decrypt
→ turn JSON bytes back into Python dict

import json
import base64
import os

from kdf import generate_salt, derive_key, create_key_from_password
from aes import encrypt, decrypt

# Konvertera bytes till ASCII string.
def bytes_to_base64(data: bytes) -> str:
    b64_bytes = base64.b64encode(data)

    return b64_bytes.decode("utf-8")

def base64_to_bytes(data: str) -> bytes:
    return base64.b64decode(data)

def create_vault() -> dict:
    return {}

def save_vault(vault: dict, password: str, file_path: str = "data.json") -> None:

    key, salt = create_key_from_password(password)
    vault_json = json.dumps(vault, indent = 4)
    vault_bytes = vault_json.encode("utf-8")
    encrypted_payload = encrypt(vault_bytes, key)

    file_data = {
        "salt": bytes_to_base64(salt)
        "nonce": bytes_to_base64(encrypted_payload["nonce"])
        "ciphertext": bytes_to_base64(encrypted_payload["ciphertext"])
    }

    with open(file_path, "w") as file:
        json.dump(file_data, file, indent = 4)






