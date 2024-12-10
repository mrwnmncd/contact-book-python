from file_parser import contact_file_manager
from structures import contact, ContactManagerError


class contact_manager:
    __contacts_store_file_path: str
    __contacts: dict[str, contact]

    def __init__(this):
        this.__contacts = {}

    def load_contacts(this, file_path: str):
        this.__contacts_store_file_path = file_path
        contact_store = contact_file_manager.from_csv(this.__contacts_store_file_path)
        for entry in contact_store:
            contact_information = this.__contacts[entry["contact_id"]] = contact()
            contact_information.contact_id = entry["contact_id"]
            contact_information.first_name = entry["first_name"]
            contact_information.middle_name = entry["middle_name"]
            contact_information.last_name = entry["last_name"]
            contact_information.birth_date = entry["birth_date"]
            contact_information.gender = entry["gender"]
            contact_information.contact_number = entry["contact_number"]
            contact_information.email_address = entry["email_address"]

    def search_contact(this, generic_search = "", **search) -> list[contact]:
        if generic_search or search.get("contact_id") or search.get("first_name") or search.get("last_name"):
            
            def is_match(test_value, search_value):
                test_values = test_value.split(" ")
                search_values = search_value.split(" ")

                for test_value in test_values:
                    for search_value in search_values:
                        if test_value.lower() == search_value.lower():
                            return True
                return False
            
            matched_contacts = []

            for contact_id, contact_information in this.__contacts.items():
                is_matched_contact_id = is_match(contact_id, generic_search) or is_match(contact_id, search.get("contact_id", ""))
                is_matched_contact_number = is_match(contact_information.contact_number, generic_search) or is_match(contact_information.contact_number, search.get("contact_number", ""))
                is_matched_email_address = is_match(contact_information.email_address, generic_search) or is_match(contact_information.email_address, search.get("email_address", ""))
                is_matched_first_name = is_match(contact_information.first_name, generic_search) or is_match(contact_information.first_name, search.get("first_name", ""))
                is_matched_last_name = is_match(contact_information.last_name, generic_search) or is_match(contact_information.last_name, search.get("last_name", ""))
                # print(is_matched_contact_id, is_matched_contact_number, is_matched_email_address, is_matched_first_name, is_matched_last_name)
                if (is_matched_contact_id or is_matched_contact_number or is_matched_email_address or is_matched_first_name or is_matched_last_name):
                    matched_contacts.append(contact_information)
        else:
            raise ValueError("Please provide a valid search criteria. Search with contact_id, first_name, or last_name.")

        return matched_contacts

    def add_contact(this, contact_information: contact):

        retreived_contacts = this.search_contact(
            contact_id=contact_information.contact_id,
            contact_number=contact_information.contact_number,
            email_address=contact_information.email_address
        )
        
        if len(retreived_contacts) > 0: 
            print(f"Incoming contact collision with an existing contact ({retreived_contacts.contact_id})")
            raise ContactManagerError("Contact already exists!")
        
        if contact_information.contact_number in [contact.contact_number for contact in this.__contacts.values()]:
            raise ContactManagerError(f"Contact of number {contact_information.contact_number} already registered! Consider updating the contact information.")
        
        if contact_information.email_address in [contact.email_address for contact in this.__contacts.values()]:
            raise ContactManagerError(f"Contact of email {contact_information.email_address} already registered! Consider updating the contact information.")
                
        
        this.__contacts.update({contact_information.contact_id: contact_information})

        contact_file_manager.to_csv(this.__contacts_store_file_path, this.__contacts)

    def update_contact(this, contact_id: str, contact_information: contact):
        
        retreived_contact = this.__contacts.get(contact_id, None)

        if retreived_contact is None:
            raise ContactManagerError(f"Contact of ID {contact_id} does not exist!")
        
        this.__contacts.update({contact_id: contact_information})

        contact_file_manager.to_csv(this.__contacts_store_file_path, this.__contacts)

    def delete_contact(this, contact_id: str) -> bool:
        
        retreived_contact = this.__contacts.get(contact_id, None)

        if retreived_contact is None:
            raise ContactManagerError(f"Contact of ID {contact_id} does not exist!")
        
        del this.__contacts[contact_id]

        contact_file_manager.to_csv(this.__contacts_store_file_path, this.__contacts)

        return True
