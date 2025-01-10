from Exceptions import *
class Account:
    def __init__(self):
        self.firstname = None
        self.lastname = None 
        self.username = None
        self.password = None
        self.signed_up = False
        self.signed_in = False
    def sign_up(self, firstname, lastname, username, password):
        try:
            if " " in username or " " in password:
                raise SearchError("Cannot have spaces in username or password.")
            
            with open("usernames_passwords", "r") as username_password_file:
                content = username_password_file.read()
                if f"{username}:" in content:
                    raise SearchError("Username already exists. Please choose another.")

            with open("firstnames", "a") as firstname_file:
                firstname_file.write(f"{firstname}\n")

            with open("lastnames", "a") as lastname_file:
                lastname_file.write(f"{lastname}\n")

            with open("usernames_passwords", "a") as username_password_file:
                username_password_file.write(f"{username}:{password}\n")
            
            self.firstname = firstname
            self.lastname = lastname
            self.username = username
            self.password = password
            self.signed_up = True
            

        except SearchError as e:
            print(f"Error: {e}")
            return "Error"
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return "Error"

    def sign_in(self, username, password):
        try:
            if not self.signed_up:
                raise SearchError("Cannot sign in because the account has not been created yet.")
            
            with open("usernames_passwords", "r") as username_password_file:
                content = username_password_file.read()
                username_password_string = f"{username}:{password}"
                if username_password_string not in content:
                    raise SearchError("Cannot find account in our database. Did you sign up?")
            
            self.signed_in = True
            print("Sign-in successful!")
            return "Success"

        except SearchError as e:
            print(f"Error: {e}")
            return "Error"
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return "Error"
