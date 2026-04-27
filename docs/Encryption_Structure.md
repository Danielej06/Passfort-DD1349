# Structure of encryption
### Argon2 & AES password manager complete structure

Argon2 and AES are used to store and retrieve passwords. 
- Argon2 is used on master password. This encryption is crucial, and used throughout all other encryption.
- AES is used to encrypt and decrypt the stored passwords.

### Core encryption idea

The system is built around a single secret:
The master password is used to derive an encryption key that protects all stored passwords. The Argon conversion will act as the ONE key.

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


