## This file is used to input the credentials and save them to the vault.
from crypto.kdf import create_key_from_password
from crypto.vault import create_vault, load_vault, save_vault
from loading import loading
from crypto.aes import encrypt, decrypt
def input_credentials(master_password):
    import os
    
    print("Enter the name of the credentials") ## This should be changed, kind of confused me. /Akanksh
    title = input()
    print("Enter the username for", title)
    username = input()
    print("Enter the password for", title)
    password = input()
    print("Enter the url for", title)
    url = input()
    ## Create a dictionary entry for the credentials
    entry = {
        "username": username,
        "password": password,
        "url": url
    }
    # Check if credentials file is there
    if os.path.isfile("data.json") == False:
        credentials = {
            title: entry
        }
    else:
        # If file is there check if it is empty
        with open('data.json', 'r') as saved_credentials:
            saved_credentials.seek(0, 2) # Move pointer to end of file
            if saved_credentials.tell() == 0:
                credentials = {
                    title: entry
                }
            else:
                ##Open data.json and read to saved_credentials
                saved_credentials.seek(0, 0) # Move pointer to start of file
                credentials = load_vault(master_password)
                ## Update credentials with the new entry
                credentials.update({title : entry})
    ##Create vault if there is no vault, then save the credentials to the vault. If there is a vault, just save the credentials to the vault.
    create_vault()
    save_vault(credentials, master_password)
    print("Credentials saved successfully!")
    loading()
    