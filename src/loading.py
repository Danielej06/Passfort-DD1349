
import time

def loading():
    text= "##################################################################"

    for cha in text:
        print(cha, end='', flush = True)
        time.sleep(0.01) ## Loading bar animation.
    print("")

## REMOVE THIS FILE WHEN IMPLEMENTING GUI. ONLY TO MAKE IT EASIER TO VIEW IN TERMINAL.