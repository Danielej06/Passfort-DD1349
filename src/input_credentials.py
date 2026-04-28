## This file is used to input the credentials and save them to a json file.
def input_credentials():
    import json
    
    print("Enter the name of the credentials")
    title = input()
    print("Enter the username for", title)
    username = input()
    print("Enter the password for", title)
    password = input()
    print("Enter the url for", title)
    url = input()
    credentials = {
        "title": title,
        "username": username,
        "password": password,
        "url": url
    }
    with open('data.json', 'w') as saved_credentials:
        json.dump(credentials, saved_credentials)
    
    print("Credentials saved successfully!")