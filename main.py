from structures import contact, ContactManagerError
from utilities import required_input
from managers import contact_manager
import re

CONTACTS_FILE = "contacts.csv"


class Application:
    contact_book: contact_manager = contact_manager()

    def __init__(this):
        this.contact_book.load_contacts(CONTACTS_FILE)

    def console_interface_find_contacts(this):
        search_query = required_input("Enter name, number, or email of contact to search: ", throw_exception=False)
        
        found_users = this.contact_book.search_contact(search_query)
        found_users_size = len(found_users)

        if found_users_size == 0:
            print("Contact record not found!")
            return
        
        if found_users_size > 1:
            print(f"{found_users_size} contacts found for {search_query}:")
            print()
        
        for user in found_users:
            print(str(user))
            print()

    def console_interface_add_contact(this):
        input_first_name = required_input("Enter First Name: ", throw_exception=False)
        input_middle_name = input("Enter Middle Name: ")
        input_last_name = required_input("Enter Last Name: ", throw_exception=False)
        input_birth_date = input("Enter Birth Date: ")
        input_gender = input("Enter Gender: ")
        input_contact_number =required_input("Enter Contact Number: ", throw_exception=False)
        while not this.__is_valid_contact_number(input_contact_number):
            print("Invalid contact number. Please enter a valid 11-digit number starting with 09.")
            input_contact_number = required_input("Enter Contact Number: ", throw_exception=False)
        input_email = required_input("Enter Email Address: ", throw_exception=False)
        while not this.__is_valid_email(input_email):
            print("Invalid email address. Please enter a valid email address.")
            input_email = required_input("Enter Email Address: ", throw_exception=False)

        

        new_user = contact()
        new_user.assign_id()
        new_user.first_name = input_first_name
        new_user.middle_name = input_middle_name
        new_user.last_name = input_last_name
        new_user.birth_date = input_birth_date
        new_user.gender = input_gender
        new_user.contact_number = input_contact_number
        new_user.email_address = input_email

        try:
            this.contact_book.add_contact(new_user)
            print("New contact registered.")
        except ContactManagerError as Error:
            print("An error occured. Contact information not registered.")
            print(Error)  # todo: print error message only

    def console_interface_update_contact(this):
        search_query = required_input("Enter name, number, or email of contact to update: ")

        found_users = this.contact_book.search_contact(search_query)
        found_user = None

        if len(found_users) == 0:
            print("Contact record not found!")
            return
        
        elif len(found_users) > 1:
            print(f"{len(found_users)} contacts found for {search_query}:")
            print()

            for user in found_users:
                print(str(user))
                print()

            contact_id = required_input("Enter Contact ID to update: ")
            found_user = this.contact_book.search_contact(contact_id=contact_id)[0]

        elif len(found_users) == 1:
            found_user = found_users[0]


        input_first_name = required_input(f"Enter First Name ({found_user.first_name}): ", default_value=found_user.first_name, throw_exception=False)
        input_middle_name = input(f"Enter Middle Name ({found_user.middle_name}): ")
        input_last_name = required_input(f"Enter Last Name ({found_user.last_name}): ", default_value=found_user.last_name, throw_exception=False)
        input_birth_date = input(f"Enter Birth Date ({found_user.birth_date}): ")
        input_gender = input(f"Enter Gender ({found_user.gender}): ")
        input_contact_number = required_input(f"Enter Contact Number ({found_user.contact_number}): ", default_value=found_user.contact_number, throw_exception=False)
        input_email = required_input(f"Enter Email Address ({found_user.email_address}): ", default_value=found_user.email_address, throw_exception=False)

        new_user = contact(
            contact_id=found_user.contact_id,
            first_name=input_first_name,
            middle_name=input_middle_name,
            last_name=input_last_name,
            birth_date=input_birth_date,
            gender=input_gender,
            contact_number=input_contact_number,
            email=input_email,
        )

        try:
            this.contact_book.update_contact(found_user.contact_id, new_user)
            print("Contact updated.")
        except ContactManagerError as Error:
            print("An error occured. Contact information not registered.")
            print(Error) # todo: print error message only
        except Exception as Error:
            print("An error occured. Contact information not registered.")
            print(Error) # todo: print error message only

    def console_interface_delete_contact(this):
        search_query = input("Enter name, number, or email of contact to delete: ")

        found_users = this.contact_book.search_contact(search_query)
        found_user = None

        if len(found_users) == 0:
            print("Contact record not found!")
            return
        
        elif len(found_users) > 1:
            print(f"{len(found_users)} contacts found for {search_query}:")
            print()

            for user in found_users:
                print(str(user))
                print()

            contact_id = required_input("Enter Contact ID to delete: ")
            found_user = this.contact_book.search_contact(contact_id=contact_id)[0]

        elif len(found_users) == 1:
            found_user = found_users[0]

        print(str(found_user))

        confirm_key = input("Are you sure to delete this contact? [y/N] ")

        if confirm_key != "y":
            print("Deletion aborted. Contact is retained.")
            return

        this.contact_book.delete_contact(found_user.contact_id)

    @staticmethod
    def __is_valid_contact_number(contact_number):
        return re.match(r'^09\d{9}$', contact_number) is not None
    
    @staticmethod
    def __is_valid_email(email):
        return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email) is not None


def console_interface():
    choice = ""
    while choice != "Q":
        print("\n")
        app = Application()
        print("Welcome to the Contact Book!")
        print("1. Find Contact")
        print("2. Add Contact")
        print("3. Modify Contact")
        print("4. Delete Contact")
        print("Q. Quit")

        choice = input("Enter your choice: ")  # Q
        print("\n")

        match choice:
            case "1":
                app.console_interface_find_contacts()
            case "2":
                app.console_interface_add_contact()
            case "3":
                app.console_interface_update_contact()
            case "4":
                app.console_interface_delete_contact()
            case "Q":
                pass
            case _:
                print("Invalid choice!")


if __name__ == "__main__":
    console_interface()
