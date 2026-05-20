## This file is used to input the credentials and save them to the vault. It will ask the user for the title of the credentials, the username, the password and the url. 
## It will then save the credentials to the vault. If there is no vault, it will create one and then save the credentials to the vault.
from crypto.vault import create_vault, load_vault, save_vault, vault_exists
from loading import loading
def input_credentials(master_password):
    
    print("Enter the URL for the credentials you want to save")
    url = input()
    print("Enter the username for", url)
    username = input()
    print("Enter the password for", url)
    password = input()
    ## Create a dictionary entry for the credentials
    entry = {
        "url": url,
        "username": username,
        "password": password
    }
    ##Create vault if there is no vault, then save the credentials to the vault. If there is a vault, just save the credentials to the vault.
    if not vault_exists():
        create_vault()
        
    save_vault(entry, master_password)
    print("Credentials saved successfully!")
    loading()
    