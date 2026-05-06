## This file is used to read one credential from the data.json file and print to the console.
from loading import loading

def read_credentials():
    import json
    ##Open data.json and read to saved_credentials
    with open('data.json', 'r') as saved_credentials:
        credentials = json.load(saved_credentials)

    i = 1
    print("Here are your saved credentials:")
    for cr_name in credentials:
        print(i, ". " , cr_name)
        i += 1
    
    choice = input("Which one would you like to view: (Have to spell it out) ") 
    if credentials[choice] == None : ## ISSUE: The "null" situation just crashes the code, needs to be fixed.
        loading()
        print("Sorry there are no credentials saved under this name")
    else :
        loading()
        print(credentials[choice])

    pass_option = input("Would you like to change your password? (y to change, anything else to not)") ## Current issue, code only accepts y and should also accept n, anything else should prompt an error
    if pass_option == "y" :
        new_pass = input("Set your new password: ")
        loading()
        credentials[choice]["password"] = new_pass
        with open('data.json', 'w') as file:
            json.dump(credentials, file, indent = 4)
        print("Done, password changed!")
    else:
        loading()
    

        

