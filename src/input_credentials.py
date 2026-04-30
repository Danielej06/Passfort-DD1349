## This file is used to input the credentials and save them to a json file.
from loading import loading
def input_credentials():
    import os
    import json
    
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
                credentials = json.load(saved_credentials)
                ## Update credentials with the new entry
                credentials.update({title : entry})
    ##Open data.json to write and save the newcredentials to the file
    with open('data.json', 'w') as saved_credentials:
        json.dump(credentials, saved_credentials, indent=4)
    
    print("Credentials saved successfully!")
    loading()
    