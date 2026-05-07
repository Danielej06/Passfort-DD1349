## This file is used to create a loading bar animation. It is used to make the user experience better when the program is loading something.It is also used to make the program look more professional.
## It is not necessary for the program to work, but it is a nice touch. It can be removed if you want to, but it is recommended to keep it for a better user experience.
import time

def loading():
    text= "##################################################################"

    for cha in text:
        print(cha, end='', flush = True)
        time.sleep(0.01) ## Loading bar animation.
    print("")

## REMOVE THIS FILE WHEN IMPLEMENTING GUI. ONLY TO MAKE IT EASIER TO VIEW IN TERMINAL.