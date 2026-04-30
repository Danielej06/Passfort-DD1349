import secrets
from argon2.low_level import hash_secret_raw, Type


# Denna fil är "Key derivation feature." Innehåller funktioner för att derivera master password
# till en hash, som senare används med AES.

# Feel free att ändra dessa värden. La in dessa som initial eftersom de supposedly är balanced.
# Hackers ska tycka det är jobbigt, men en user ska inte spendera 20 minuter för att hämta lösenord.
salt_length = 16
time_cost = 3
memory_cost = 65536 # 64 MB
parallelism = 2
hash_len = 32 # Samma storlek som AES-256

# Genererar salt värde. Detta görs via secret importen. 
# Funktionen returnar en random byte string med salt_length många bytes.
def generate_salt() -> bytes:
    return secrets.token_bytes(salt_length)

# Konverterar lösenordet till bytes. Detta används sen för att skapa vår key, inom hash_secret_raw.
def derive_key(password: str, salt: bytes) -> bytes:

    master_Password_Bytes = password.encode("utf-8")

    key = hash_secret_raw(
    secret = master_Password_Bytes, 
    salt = salt,
    time_cost = time_cost,
    memory_cost = memory_cost,
    parallelism = parallelism,
    hash_len = hash_len,
    type = Type.ID,
    )
    return key

def create_key_from_password (password: str) -> tuple[bytes, bytes]:
    salt = generateSalt()
    key = deriveKey(master_Password, salt)
    return key, salt
