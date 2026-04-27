# Structure of encryption
### Argon2 & AES password manager complete structure

Argon2 and AES are used to store and retrieve passwords. 
- Argon2 is used on master password. This encryption is crucial, and used throughout all other encryption.
- AES is used to encrypt and decrypt the stored passwords.

### Core encryption idea

The system is built around a single secret:
The master password is used to derive an encryption key that protects all stored passwords. The Argon conversion will act as the ONE key.
The encryption key will never be stored. Hence, if an un-invited user gets into the system, no passwords will be leaked, unless the user knows the master password.

### Unlocking manager

User enters their master password:
Masters password -> Argon2 ID -> Encryption Key

The encryption key is never stored.
It is derived from the master password that has been handled through Argon2.

### Storing 

When saving a password, you must first input it. 
Input -> AES encryption of input using Encryption Key (see unlocking manager) -> Ciphered text.
Notes:
The plaintext password is never stored
The encryption key is never stored

### Retrieving a Password

When the user wishes to access a password:
Master Password -> Argon2 ID -> Encrypted key
Encrypted key + ciphered text -> AES Decryption -> Plainword password

The decrypted password is then:
- Temporarily held in memory
- Optionally copied to clipboard

