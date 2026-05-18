# Följande fil skapas för att se till att en användare blir utloggad om de är inaktiva.
# Detta är ett tillägg som är nödvändigt för att säkerställa säkerheten av programmet.
import time
# 2 minuter av inactivity innan man loggas ut
LOGOUT_TIME = 5 

# Återställer timern. Detta ska ske varje gång användaren interagerar. Denna används bara för första.
USER_ACTIVE = time.time()

class SessionManager:
    def __init__(self, started=False, logout_time=LOGOUT_TIME):
        self.logout_time = logout_time
        self.started = started
        self.user_active = time.time()
        self.key = None

    # Återställer timern, men som funktion. Enklare att calla på.
    def reset_time(self):
        self.user_active = time.time()
        
    def session_started(self):
        self.started = True
        self.reset_time()

    # Funktionen returnerar en bool beroende på tillståndet av USER_ACTIVE.
    # True om LOGOUT_TIME har gått. False om det fortfarande finns tid kvar.
    def session_state_expiry(self) -> bool:
        inactivity = time.time() - self.user_active
        compare = self.logout_time - inactivity
        if compare > 0:
            return False
        elif compare <= 0:
            self.started = False
            return True

    # Returnerar tiden innan du loggas ut. Bra att ha för något som "You will be logged out in 15 seconds".
    def time_left_before_logout(self):
        inactivity = time.time() - self.user_active
        remaining = self.logout_time - inactivity
        # Använder max för att undvika negativa int on return. Om det är negativt, returnerar den 0 istället.
        return max(0, int(remaining))





