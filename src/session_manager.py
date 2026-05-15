# Följande fil skapas för att se till att en användare blir utloggad om de är inaktiva.
# Detta är ett tillägg som är nödvändigt för att säkerställa säkerheten av programmet.


import time


# 2 minuter av inactivity innan man loggas ut
LOGOUT_TIME = 120 

# Återställer timern. Detta ska ske varje gång användaren interagerar. Denna används bara för första.
USER_ACTIVE = time.time()

# Återställer timern, men som funktion. Enklare att calla på.
def reset_time() -> None:
    global USER_ACTIVE # Så vi alltid arbetar med samma USER_ACTIVE
    USER_ACTIVE = time.time()

# Funktionen returnerar en bool beroende på tillståndet av USER_ACTIVE.
# True om LOGOUT_TIME har gått. False om det fortfarande finns tid kvar.
def session_state_expiry() -> bool:
    inactivity = time.time() - USER_ACTIVE
    compare = LOGOUT_TIME - inactivity
    if compare > 0:
        return False
    elif compare <= 0:
        return True

# Returnerar tiden innan du loggas ut. Bra att ha för något som "You will be logged out in 15 seconds".
def time_left_before_logout() -> int:
    inactivity = time.time() - USER_ACTIVE
    remaining = LOGOUT_TIME - inactivity

    # Använder max för att undvika negativa int on return.
    return max(0, int(remaining))






