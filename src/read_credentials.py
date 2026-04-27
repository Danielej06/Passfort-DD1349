def read_credentials():
    import json
    with open('data.json', 'r') as saved_credentials:
        credentials = json.load(saved_credentials)
    print(credentials)