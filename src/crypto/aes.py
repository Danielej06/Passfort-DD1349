# Struktur innan jag börjar skriva
# Vi har 32 byte hash från kdf
# Denna fil ska ta ett normalt lösenord, enkryptera med kdf hashet, och ge vår ciphertext + nonce
# Dessutom ska denna fil ha inversen till denna funktion tillgänglig.

import secrets
from cryptography.hazmat.primitives.ciphers.aead import AESGCM # Fernet är supposedly mycket enklare.
# Den ska tydligen kunna göra allt detta direkt, men då lär jag mig inget så försöker med denna istället.

# Genererar ett värde som endast används en gång. Matchas med lösenordet 
def generate_nonce() -> bytes:

    return secrets.token_bytes(12)    

# Enkrypterar lösenordet. Returnerar en dictionary med ciphertext samt number used once (nonce).
def encrypt(data: bytes, key: bytes) -> dict:
    nonce = generate_nonce()
    
    aes = AESGCM(key)
    ciphertext = aes.encrypt(nonce, data, None)
    encrypted_data = {
        "ciphertext": ciphertext,
        "nonce": nonce
    }

    return encrypted_data
    

# Dekrypterar ciphertexten. Inversen till "encrypt" funktionen. Returnerar lösenordet i läsbar text.
def decrypt(payload: dict, key: bytes) -> bytes:


    aes = AESGCM(key)
    ciphertext = payload["ciphertext"]
    nonce = payload["nonce"]
    
    plaintext = aes.decrypt(nonce, ciphertext, None)

    return plaintext

