from kdf import create_key_from_password
from aes import encrypt, decrypt

key, salt = create_key_from_password("test123")

data = b"hello secret world"

payload = encrypt(data, key)
plaintext = decrypt(payload, key)

print(plaintext)
print(plaintext == data)
print(len(payload["nonce"]))