## This file is used to read one credential from the data.json file and print to the console.

def read_credentials():
    import json
    ##Open data.json and read to saved_credentials
    with open('data.json', 'r') as saved_credentials:
        credentials = json.load(saved_credentials)
    print(credentials)