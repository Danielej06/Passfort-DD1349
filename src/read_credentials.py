## This file is used to read one credential from the vault and print to the console aswell as changing the password.
from crypto.vault import load_urls, load_vault, update_vault
from loading import loading

def read_credentials(master_password):
    ## Open the vault and read the contents to saved_credentials
    urls = load_urls()
    if urls == [] :
        print("Sorry there are no credentials saved yet. Returning to main menu.")
        return

    i = 1
    print("Here are your saved credentials:")
    for cr_name in urls:
        print(i, ". URL: " , cr_name[0], "Username: " , cr_name[1])
        i += 1
    
    choice = input("Which number would you like to view: ")
    while True:
        try:
            choice = int(choice)
            if choice < 1 or choice > len(urls):
                raise ValueError
            break
        except ValueError:
            choice = input("Invalid choice, please enter a number between 1 and " + str(len(urls)) + ": ")
    ## Check if the choice is valid, if not return to main menu. If it is valid, print the credentials.
    
    try:
        credentials = load_vault(master_password, choice)
    except KeyError:
        loading()
        print("Sorry there are no credentials saved under this name")
        return 
    loading()
    print(credentials)

    pass_option = input("Would you like to change your password? (y to change, anything else to not) ") ## Current issue, code only accepts y and should also accept n, anything else should prompt an error (is this really necessary? maybe just accept y and that anything else should be treated as n)
    if pass_option == "y" :
        new_pass = input("Set your new password: ")
        loading()
        credentials["password"] = new_pass
        ##Save the new password to the vault
        update_vault(credentials, master_password, choice)
        print("Done, password changed!")
    else:
        loading()
    

        

