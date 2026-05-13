## This is the main file for the password manager application. It will handle the user input and call on the required functions to read and write credentials to the vault.
from crypto.vault import vault_exists
from read_credentials import read_credentials
from input_credentials import input_credentials
from loading import loading
from crypto.masterpassword import create_master_password, verify_master_password
def main():
    while True:
        print("Welcome to the password manager!")
        if not vault_exists():
            print("It seems like you don't have a vault yet. Let's create one!")
            master_password = create_master_password()
            loading()
        else:
            print("First you will have to enter your master password to access your credentials.")
            master_password = input("Enter your master password: ")
            loading()
            if not verify_master_password(master_password):
                print("Incorrect master password or corrupted vault file, please try again.")
                continue
            print("Master password accepted!")
        print("What would you like to do?")
        print("1. Add new credentials")
        print("2. View saved credentials")
        print("3. Exit")
        choice = input("Please enter your choice: ")
        if choice == "1":
            loading()
            print("")
            input_credentials(master_password)
        elif choice == "2":
            loading()
            print("")
            read_credentials(master_password)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")
main()