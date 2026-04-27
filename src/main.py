## This is the main file for the password manager application. It will handle the user input and save the credentials to a file.

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
print("Credentials saved successfully!")