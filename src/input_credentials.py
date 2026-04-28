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
    # Check if credentials file is there
    if os.path.isfile("data.json") == False:
        credentials = {
            title: {
                "username": username,
                "password": password,
                "url": url
            }
        }
    else:
        with open('data.json', 'r') as saved_credentials:
            credentials = json.load(saved_credentials)
        credentials[title] = {
                "username": username,
                "password": password,
                "url": url
        }
    ##open data.json to write and save credentials to the file
    with open('data.json', 'w') as saved_credentials:
        json.dump(credentials, saved_credentials)
    
    print("Credentials saved successfully!")