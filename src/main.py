## This is the main file for the password manager application. It will handle the user input and save the credentials to a file aswell as retrieve the credentials.
from read_credentials import read_credentials
from input_credentials import input_credentials
def main():
    while True:
        print("Welcome to the password manager!")
        print("1. Add new credentials")
        print("2. View saved credentials")
        print("3. Exit")
        choice = input("Please enter your choice: ")
        if choice == "1":
            input_credentials()
        elif choice == "2":
            read_credentials()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")
main()