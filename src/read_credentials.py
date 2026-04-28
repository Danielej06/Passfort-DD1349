## This file is used to read the credentials from the data.json file and print them to the console.
def read_credentials():
    import json
    with open('data.json', 'r') as saved_credentials:
        credentials = json.load(saved_credentials)
    print(credentials)