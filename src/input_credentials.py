## This file is used to input the credentials and save them to a json file.
def input_credentials():
    import os
    import json
    
    print("Enter the name of the credentials")
    title = input()
    print("Enter the username for", title)
    username = input()
    print("Enter the password for", title)
    password = input()
    print("Enter the url for", title)
    url = input()
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
        with open('data.json', 'r') as saved_credentials:
            saved_credentials.seek(0, 2) # Move pointer to end of file
            if saved_credentials.tell() == 0:
                credentials = {
                    title: entry
                }
            else:
                saved_credentials.seek(0, 0) # Move pointer to start of file
                credentials = json.load(saved_credentials)
                credentials.update({title : entry})
    ##open data.json to write and save credentials to the file
    with open('data.json', 'w') as saved_credentials:
        json.dump(credentials, saved_credentials, indent=4)
    
    print("Credentials saved successfully!")