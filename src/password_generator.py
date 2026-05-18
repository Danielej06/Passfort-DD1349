import secrets
import string

# Massiv string som innehåller alla möjliga bokstäver, symboler och nummer som kan användas i lösenordet.
POTENTIAL_CHARACTERS = (
    string.ascii_uppercase +
    string.ascii_lowercase +
    string.digits + 
    string.punctuation
    )

# Genererar ett starkt, troligen unikt lösenord, med 20-26 characters.
def strong_password_generator() -> str:
    pass_length = secrets.randbelow(7) + 20 # 20-26 characters borde vara tillräckligt
    
    password = ""

    for x in range(pass_length):
        password += secrets.choice(POTENTIAL_CHARACTERS)

        
    return password
