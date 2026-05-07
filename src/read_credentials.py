## This file is used to read one credential from the vault and print to the console aswell as changing the password.
from crypto.vault import load_vault, save_vault
from loading import loading

def read_credentials(master_password):
    ## Open the vault and read the contents to saved_credentials
    if load_vault(master_password) == {} : ## ISSUE: The "null" situation just crashes the code, needs to be fixed.
        print("Sorry there are no credentials saved yet. Returning to main menu.")
        return
    credentials = load_vault(master_password)

    i = 1
    print("Here are your saved credentials:")
    for cr_name in credentials:
        print(i, ". " , cr_name)
        i += 1
    
    choice = input("Which one would you like to view: (Have to spell it out) ")
    ## Check if the choice is valid, if not return to main menu. If it is valid, print the credentials.
    try:        credentials[choice]
    except KeyError:
        loading()
        print("Sorry there are no credentials saved under this name")
        return 
    loading()
    print(credentials[choice])

    pass_option = input("Would you like to change your password? (y to change, anything else to not)") ## Current issue, code only accepts y and should also accept n, anything else should prompt an error (is this really necessary? maybe just accept y and that anything else should be treated as n)
    if pass_option == "y" :
        new_pass = input("Set your new password: ")
        loading()
        credentials[choice]["password"] = new_pass
        ##Save the new password to the vault
        save_vault(credentials, master_password)
        print("Done, password changed!")
    else:
        loading()
    

        

