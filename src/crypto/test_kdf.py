from kdf import generate_salt, derive_key, create_key_from_password
key, salt = create_key_from_password("test123")

print(len(key))   # should be 32
print(len(salt))  # should be 16

same_salt = generate_salt()

key1 = derive_key("test123", same_salt)
key2 = derive_key("test123", same_salt)
key3 = derive_key("wrongpassword", same_salt)

print(key1 == key2)  # should be True
print(key1 == key3)  # should be False